from core.serializers import (regex_match,
                              datetime,
                              REGEX_UUID,
                              Documents,
                              DocumentAuthAccessSerializer,
                              ValidationError)


class DocumentCreateSerializer(DocumentAuthAccessSerializer):
    class Meta:
        model = DocumentAuthAccessSerializer.Meta.model
        fields = DocumentAuthAccessSerializer.Meta.fields + ("site",
                                                           "protocol",
                                                           "username",
                                                           "password",
                                                           "description",)

    def validate(self, data: dict) -> dict:
        super(DocumentCreateSerializer, self).validate(data=data)

        site: str | None = data.get("site", None)
        protocol: str | None  = data.get("protocol", None)
        username: str | None  = data.get("username", None)
        license_info: dict = self._account.get_license_information()
        current_doc_num: int = len(Documents.objects(account=self._account.uuid))

        if license_info != {}:
            if current_doc_num >= license_info.get("kryptos_license").get("documents"):
                raise ValidationError("you reached license limit.")

            elif datetime.now() < license_info.get("kryptos_license_issued"):
                raise ValidationError("license is not valid.")

            elif datetime.now() > license_info.get("kryptos_license_expire"):
                raise ValidationError("license has been expired.")

        else:
            if current_doc_num >= 5:
                raise ValidationError("you reached license limit.")

        if Documents.objects(account=self._account.uuid,
                             site=site,
                             protocol=protocol,
                             username=username).first() is not None:
            raise ValidationError("document is already created.")

        return data


    def save(self):
        new_doc = Documents(account=self._account.uuid, **self.validated_data)
        new_doc.save(code=self._account.get_code())


class DocumentGetInfoSerializer(DocumentAuthAccessSerializer):
    def __init__(self, *args, **kwargs):
        self.__uuid = kwargs.pop("uuid", None)
        self._document = None
        super().__init__(*args, **kwargs)

    def validate(self, data:dict) -> dict:
        super(DocumentGetInfoSerializer, self).validate(data=data)

        self._document = Documents.objects(account=self._account.uuid, uuid=self.__uuid).first()
        if self._document is None:
            raise ValidationError("document is not exist")

        return data

    def save(self):
        return self._account._asterisk_doc(document=self._document)


class DocumentDeleteSerializer(DocumentGetInfoSerializer):
    def save(self):
        self._document.delete()


class DocumentUpdateSerializer(DocumentGetInfoSerializer):
    class Meta:
        model = DocumentGetInfoSerializer.Meta.model
        fields = DocumentGetInfoSerializer.Meta.fields + ("site",
                                                          "protocol",
                                                          "username",
                                                          "description",)

    def validate(self, data:dict) -> dict:
        super(DocumentUpdateSerializer, self).validate(data=data)

        site = data.get("site", None)
        protocol = data.get("protocol", None)
        username = data.get("username", None)
        description = data.get("description", None)
        license_info: dict = self._account.get_license_information()

        if license_info != {}:
            if datetime.now() < license_info.get("kryptos_license_issued"):
                raise ValidationError("license is not valid.")

            elif datetime.now() > license_info.get("kryptos_license_expire"):
                raise ValidationError("license has been expired.")

        tmp_document = Documents.objects(account=self._account.uuid,
                             site=site if site is not None else self._document.site,
                             protocol=protocol if protocol is not None else self._document.protocol,
                             username=username if username is not None else self._document.username,
                             description=description if description is not None else self._document.description).first()

        if tmp_document == self._document:
            raise ValidationError("there is no update on your document.")

        if tmp_document != self._document and tmp_document is not None:
            raise ValidationError("document is already created.")

        return data

    def save(self) -> None:
        self._document.modify(**self.validated_data)
        return None


class DocumentPasswordUpdateSerializer(DocumentGetInfoSerializer):
    class Meta:
        model = DocumentGetInfoSerializer.Meta.model
        fields = DocumentGetInfoSerializer.Meta.fields + ("password",)


    def __init__(self, *args, **kwargs):
        self.__new_password = None
        super(DocumentPasswordUpdateSerializer, self).__init__(*args, **kwargs)


    def validate(self, data:dict) -> dict:
        super(DocumentPasswordUpdateSerializer, self).validate(data=data)

        self.__new_password = self.initial_data.get("new_password", None)

        if self.__new_password is None:
            raise ValidationError("you have to input a new password.")

        if len(self.__new_password) < 8:
            raise ValidationError("password must be at least 8 characters.")

        if not self._document.check_password(code=self._account.get_code(),
                                             password=data.get("password")):
            raise ValidationError("current password is not match.")

        return data


    def save(self) -> None:
        if self.__new_password != self.validated_data.get("password", None):
            self._document.modify(**{"password": self.__new_password})
            self._document.save(code=self._account.get_code())

        return None


class DocumentsListGetInfoSerializer(DocumentAuthAccessSerializer):
    def __init__(self, *args, **kwargs):
        self.__search_q = kwargs.pop("search_q", None)
        super(DocumentsListGetInfoSerializer, self).__init__(*args, **kwargs)


    def save(self):
        contain_fields_list = ["site", "description"]
        trimmed_data = { f"{k}__icontains" if k in contain_fields_list else k :v for k,v in self.__search_q.items() }

        doc_list = Documents.objects(account=self._account.uuid, **trimmed_data)
        if self._chat_info is not None:
            return [ {"uuid": doc.uuid, "description": doc.description} for doc in doc_list ]

        return [ doc.uuid for doc in doc_list ]


class DocumentsListDeleteSerializer(DocumentAuthAccessSerializer):
    def __init__(self, *args, **kwargs):
        self.__docs_uuid_list = kwargs.pop("docs_uuid_list", None)
        super(DocumentsListDeleteSerializer, self).__init__(*args, **kwargs)


    def validate(self, data:dict) -> dict:
        super(DocumentsListDeleteSerializer, self).validate(data=data)

        for uuid in self.__docs_uuid_list:
            if not regex_match(pattern=REGEX_UUID, string=uuid):
                raise ValidationError("there is a non UUID string in your request.")

        return data


    def save(self):
        for uuid in self.__docs_uuid_list:
            tmp_doc = Documents.objects(account=self._account.uuid, uuid=uuid).first()
            tmp_doc.delete() if tmp_doc is not None else None


class DocumentsStatisticsSerializer(DocumentAuthAccessSerializer):

    def save(self):
        return self._account.get_documents_statistics()
