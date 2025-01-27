
APP_NAME: str = "Kryptos"


PROMPT_API_ACTIVATE: dict = {
    "en": {
        "success": "✅ Your account has been activated.",
        "fail": "⛔ The activation code does not match.\nPlease check your email again.",
    },
    "ja": {
        "success": "✅ アカウントが有効化されました。",
        "fail": "⛔ 有効化コードが一致しません。\nメールを再度確認してください。",
    },
    "ko": {
        "success": "✅ 계정이 활성화되었습니다.",
        "fail": "⛔ 활성화 코드가 일치하지 않습니다.\n다시 메일을 확인해주세요.",
    }
}
PROMPT_API_CHANGE_PASSWORD: dict = {
    "en": {
        "success": f"✅ The password for your {APP_NAME} account has been successfully changed.\nPlease log in again.",
        "fail": f"❌ Failed to change the password for your {APP_NAME} account.\nPlease make sure the current password is correct."
    },
    "ja": {
        "success": f"✅ {APP_NAME}アカウントのパスワードが正常に変更されました。\n再度ログインしてください。",
        "fail": f"❌ {APP_NAME}アカウントのパスワード変更に失敗しました。\n現在のパスワードが正しいか確認してください。"
    },
    "ko": {
        "success": f"✅ {APP_NAME} 계정 비밀번호가 변경되었습니다.\n다시 로그인 해주시기 바랍니다.",
        "fail": f"❌ {APP_NAME} 계정 비밀번호 변경에 실패했습니다.\n현재 사용중인 비밀번호가 맞는지 확인해주세요."
    }
}
PROMPT_API_CHANGE_PASSWORD_DOC: dict = {
    "en": {
        "success": "✅ The account password has been successfully changed.",
        "fail": "⛔ Failed to change the account password.\nPlease make sure the previously registered password is correct."
    },
    "ja": {
        "success": "✅ アカウントのパスワードが正常に変更されました。",
        "fail": "⛔ アカウントのパスワードの変更に失敗しました。\n以前に登録したパスワードが正しいか確認してください。"
    },
    "ko": {
        "success": "✅ 계정 비밀번호 변경이 완료되었습니다.",
        "fail": "⛔ 계정 비밀번호 변경에 실패하였습니다.\n기존에 등록된 계정 비밀번호가 정확한지 확인해주세요."
    }
}
PROMPT_API_CREATE_DOC: dict = {
    "en": {
        "success": "✅ The new account information has been successfully registered.",
        "fail": "⛔ Failed to register new account information.\n",
        "duplicate": "⚠️ An account with the same site and ID already exists.",
        "license_invalid": "⚠️ The registered license is not yet valid.",
        "license_expire": "⚠️ The registered license has expired.",
        "reach_limit": "⚠️ The registration limit of the license has been reached."
    },
    "ja": {
        "success": "✅ 新しいアカウント情報が正常に登録されました。",
        "fail": "⛔ 新しいアカウント情報の登録に失敗しました。\n",
        "duplicate": "⚠️ 同じサイトとIDで登録されたアカウントが存在します。",
        "license_invalid": "⚠️ 登録されたライセンスはまだ有効ではありません。",
        "license_expire": "⚠️ 登録されたライセンスは有効期限が切れています。",
        "reach_limit": "⚠️ ライセンスの登録可能な上限に達しました。"
    },
    "ko": {
        "success": "✅ 새 계정 정보를 정상적으로 등록하였습니다.",
        "fail": "⛔ 새 계정 정보 등록에 실패하였습니다.\n",
        "duplicate": "⚠️ 동일한 사이트 및 ID로 등록된 계정이 존재합니다.",
        "license_invalid": "⚠️ 등록된 라이센스가 아직 유효하지 않습니다.",
        "license_expire": "⚠️ 등록된 라이센스가 만료되었습니다.",
        "reach_limit": "⚠️ 라이센스의 등록 가능 한도에 도달했습니다. "
    }
}
PROMPT_API_DELETE_KRYPTOS: dict = {
    "en": {
            "success": f"✅ Your {APP_NAME} account has been successfully deleted.\n🫂 Thank you for using {APP_NAME}.",
            "fail": f"❌ Failed to delete your {APP_NAME} account.\nPlease check if you entered the correct password."
        },
        "ja": {
            "success": f"✅ {APP_NAME}アカウントが正常に削除されました。\n🫂 {APP_NAME}をご利用いただきありがとうございました。",
            "fail": f"❌ {APP_NAME}アカウントの削除に失敗しました。\n正しいパスワードを入力したか確認してください。"
        },
        "ko": {
            "success": f"✅ {APP_NAME} 계정이 정상적으로 삭제되었습니다.\n🫂 {APP_NAME}를 사용해주셔서 감사합니다.",
            "fail": f"❌ {APP_NAME} 계정 삭제가 실패했습니다.\n올바른 비밀번호를 입력했는지 다시 확인해주세요."
        }
}
PROMPT_API_DELETE_DOC: dict = {
    "en": {
        "success": "✅ Successfully deleted the registered account.",
        "fail": "⛔ Failed to delete the registered account."
    },
    "ja": {
        "success": "✅ 登録済みのアカウントを正常に削除しました。",
        "fail": "⛔ 登録済みのアカウントの削除に失敗しました。"
    },
    "ko": {
        "success": "✅ 등록 계정 삭제를 완료했습니다.",
        "fail": "⛔ 등록 계정 삭제에 실패했습니다."
    }
}
PROMPT_API_DOC_STATISTICS: dict = {
    "en": {
        "success": "✅ The current security statistics for the registered accounts are as follows:",
        "fail": "⛔ Failed to retrieve security statistics for the registered accounts.",
        "total": "Total number of registered accounts",
        "length": "Passwords with fewer than 8 characters",
        "upper": "Passwords without uppercase letters",
        "lower": "Passwords without lowercase letters",
        "special": "Passwords without special characters",
        "digit": "Passwords without digits",
        "period": "Passwords unchanged for over 90 days",
        "continue": "To continue, please click the 'Skip' button."
    },
    "ja": {
        "success": "✅ 登録済みアカウントのセキュリテイ統計情報は以下の通りです。",
        "fail": "⛔ 登録済みアカウントのセキュリテイ統計情報の取得に失敗しました。",
        "total": "登録済みアカウントの総数",
        "length": "8文字未満のパスワードの数",
        "upper": "大文字を含まないパスワードの数",
        "lower": "小文字を含まないパスワードの数",
        "special": "特殊文字を含まないパスワードの数",
        "digit": "数字を含まないパスワードの数",
        "period": "90日以上変更されていないパスワードの数",
        "continue": "続行するには「スキップ」ボタンをクリックしてください。"
    },
    "ko": {
        "success": "✅ 현재 등록된 계정의 보안 통계는 아래와 같습니다.",
        "fail": "⛔ 등록 계정의 보안 통계 정보 호출에 실패하였습니다.",
        "total": "전체 등록 계정 수",
        "length": "8자리 미만 비밀번호 수",
        "upper": "대문자 미포함 비밀번호 수",
        "lower": "소문자 미포함 비밀번호 수",
        "special": "특수문자 미포함 비밀번호 수",
        "digit": "숫자 미포함 비밀번호 수",
        "period": "90일 이상 미변경 비밀번호 수",
        "continue": "계속하려면 '건너뛰기' 버튼을 클릭해 주세요."
    }
}
PROMPT_API_GET_DOC: dict = {
    "en": {
        "site": "Site",
        "username": "Username",
        "password": "Password",
        "description": "Description",
        "success": "✅ The information of the selected account is as follows.",
        "fail": "⛔ Failed to retrieve the selected account information.",
        "question": "What action would you like to take with the selected account?"
    },
    "ja": {
        "site": "サイト",
        "username": "アカウント",
        "password": "パスワード",
        "description": "説明",
        "success": "✅ 選択したアカウントの情報は以下の通りです。",
        "fail": "⛔ 選択したアカウント情報の取得に失敗しました。",
        "question": "選択したアカウントでどのような操作を行いますか？"
    },
    "ko": {
        "site": "사이트",
        "username": "ID/계정명",
        "password": "비밀번호",
        "description": "설명",
        "success": "✅ 선택한 계정의 정보는 아래와 같습니다.",
        "fail": "⛔ 선택한 계정 정보 호출에 실패하였습니다.",
        "question": "선택한 계정으로 어떤 작업을 진행하시겠습니까?"
    }
}

PROMPT_API_REGISTER_LICENSE: dict = {
    "en": {
        "success": "✅ The license has been successfully registered.",
        "fail": "⛔ Failed to register the license.",
        "invalid": "This is not a valid license file.",
        "mismatch_account": "The license cannot be applied to the current account."
    },
    "ja": {
        "success": "✅ ライセンスが正常に登録されました。",
        "fail": "⛔ ライセンスの登録に失敗しました。",
        "invalid": "有効なライセンスファイルではありません。",
        "mismatch_account": "現在のアカウントに適用できないライセンスです。"
    },
    "ko": {
        "success": "✅ 라이센스가 정상적으로 등록되었습니다. ",
        "fail": "⛔ 라이센스 등록에 실패하였습니다.",
        "invalid": "유효한 라이센스 파일이 아닙니다.",
        "mismatch_account": "현재 계정에 적용할 수 없는 라이센스입니다.",
    }
}
PROMPT_API_SENDCODE: dict = {
    "en": {
        "success": "✅ The activation code has been successfully sent to your registered email.",
        "fail": "❌ The email was not sent."
    },
    "ja": {
        "success": "✅ 登録メールに有効化コードの送信が完了しました。",
        "fail": "❌ メールが送信されませんでした。"
    },
    "ko": {
        "success": "✅ 가입 메일로 활성화 코드 전송을 완료했습니다.",
        "fail": "❌ 메일이 전송되지 않았습니다."
    }
}
PROMPT_API_SEARCH_DOCS: dict = {
    "en": {
        "success": "✅ Found a total of {} search results.\nPlease select the result you want to view.",
        "no_data": "🤔 No search results found.",
        "fail": "❌ Failed to retrieve the results."
    },
    "ja": {
        "success": "✅ 合計 {} 件の検索結果が見つかりました。\n表示する結果を選択してください。",
        "no_data": "🤔 検索結果が見つかりませんでした。",
        "fail": "❌ 結果の取得に失敗しました。"
    },
    "ko": {
        "success": "✅ 총 {} 건의 검색 결과가 있습니다.\n조회할 결과를 선택해주세요.",
        "no_data": "🤔 검색 결과가 존재하지 않습니다.",
        "fail": "❌ 결과 호출에 실패하였습니다.",
    }
}
PROMPT_API_SIGNIN: dict = {
    "en": {
        "success": "✅ success to sign in.",
        "fail": "⛔ fail to sign in.",
        "question_signup": f"📄 Not a {APP_NAME} Member? You want to sign in?"
    },
    "ja": {
        "success": "✅ サインインに成功しました。",
        "fail": "⛔ サインインに失敗しました。",
        "question_signup": f"📄 {APP_NAME}メンバーではありませんか？サインアップしますか？"
    },
    "ko": {
        "success": "✅ 로그인에 성공했습니다.",
        "fail": "⛔ 로그인에 실패했습니다.",
        "question_signup": f"📄 {APP_NAME} 회원이 아니신가요? 가입하시겠습니까?"
    },
}
PROMPT_API_SIGNOUT: dict = {
     "en": {
        "success": "✅ Successfully logged out.",
        "fail": "⛔ Failed to log out."
    },
    "ja": {
        "success": "✅ ログアウトに成功しました。",
        "fail": "⛔ ログアウトに失敗しました。"
    },
    "ko": {
        "success": "✅ 성공적으로 로그아웃 되었습니다.",
        "fail": "⛔ 로그아웃에 실패했습니다."
    }
}
PROMPT_API_SIGNUP: dict = {
    "en": {
        "success": f"✅ success to sign up to {APP_NAME}.",
        "fail": "⛔ fail to sign  up.",
        "duplicate_account": "already registered email address.",
        "allow_one_account": "You cannot create more than one account in a single chat. An account is already registered.",
    },
    "ja": {
        "success": f"✅ {APP_NAME}のサインアップに成功しました。",
        "fail": "⛔ サインアップに失敗しました。",
        "duplicate_account": "既に登録されているメールアドレスです。",
        "allow_one_account": "1つのチャット内で複数のアカウントを作成することはできません。既に登録済みのアカウントが存在します。",
    },
    "ko": {
        "success": f"✅ {APP_NAME} 회원가입에 성공했습니다.",
        "fail": "⛔ 회원가입에 실패했습니다.",
        "duplicate_account": "이미 등록된 이메일 주소입니다.",
        "allow_one_account": "하나의 채팅창에서 두 개 이상의 계정을 생성할 수 없습니다.\n이미 등록된 계정이 존재합니다.",
    }
}
PROMPT_API_UPDATE_ACCOUNT: dict = {
    "en": {
        "success": "✅ Settings information has been updated.",
        "fail": "⛔ Failed to update settings information."
    },
    "ja": {
        "success": "✅ 設定情報が更新されました。",
        "fail": "⛔ 設定情報の更新に失敗しました。"
    },
    "ko": {
        "success": "✅ 설정 정보가 수정되었습니다.",
        "fail": "⛔ 설정 정보 수정에 실패하였습니다."
    }
}
PROMPT_API_UPDATE_DOC: dict = {
    "en": {
        "duplicate": "⚠️ The updated information already exists.",
        "success": "✅ The information for the account has been updated.",
        "fail": "⛔ Failed to update the account information.",
        "license_invalid": "⚠️ The registered license is not yet valid.",
        "license_expire": "⚠️ The registered license has expired.",
        "no_change": "⚠️ No changes detected.",
    },
    "ja": {
        "duplicate": "⚠️ 更新された情報は既に存在します。",
        "success": "✅ アカウント情報が更新されました。",
        "fail": "⛔ アカウント情報の更新に失敗しました。",
        "license_invalid": "⚠️ 登録されたライセンスはまだ有効ではありません。",
        "license_expire": "⚠️ 登録されたライセンスは有効期限が切れています。",
        "no_change": "⚠️ 変更点が検出されませんでした。",
    },
    "ko": {
        "duplicate": "⚠️ 변경한 내역과 동일한 정보가 존재합니다.",
        "success": "✅ 해당 계정의 정보가 수정되었습니다.",
        "fail": "⛔  해당 계정의 정보 수정에 실패하였습니다.",
        "license_invalid": "⚠️ 등록된 라이센스가 아직 유효하지 않습니다.",
        "license_expire": "⚠️ 등록된 라이센스가 만료되었습니다.",
        "no_change": "⚠️ 변경 사항이 없습니다.",
    }
}

PROMPT_ACTIVATE: dict = {
    "en": {
        "intro": "Click the send button to deliver the activation code to your registered email.",
        "guide": "Enter the activation code sent to your email in the input field below.",
        "placeholder": "Activation Code - 6 Characters",
        "code_invalidate": "❌ The activation code must be 6 characters long."
    },
    "ja": {
        "intro": "登録したメールに有効化コードを送信するには、送信ボタンをクリックしてください。",
        "guide": "メールで送信された有効化コードを下の入力欄に入力してください。",
        "placeholder": "有効化コード - 6字入力",
        "code_invalidate": "❌ 有効化コードは6文字で入力する必要があります。"
    },
    "ko": {
        "intro": "가입한 메일로 활성화 코드를 전달하려면 전송 버튼을 클릭해 주세요.",
        "guide": "메일로 전송된 활성화 코드를 아래의 입력창에 입력해 주세요.",
        "placeholder": "활성화 코드 입력 - 6자리",
        "code_invalidate": "❌ 활성화 코드는 6자리가 입력되어야 합니다."
    }
}
PROMPT_CHECK_DELETE_DOC: dict = {
    "en": {
        "intro": "⚠️ Do you want to delete this account information?"
    },
    "ja": {
        "intro": "⚠️ このアカウント情報を削除しますか？"
    },
    "ko": {
        "intro": "⚠️ 이 계정 정보를 삭제하시겠습니까?"
    }
}
PROMPT_CHECK_SIGNUP: dict = {
    "en": {
        "intro": "Sign Up Info",
        "email": "Email",
        "first_name": "First Name",
        "last_name": "Last Name",
        "final_check": "Please review the information you entered.\nShall we proceed with the registration?",
    },
    "ja": {
        "intro": "登録情報",
        "email": "メールアドレス",
        "first_name": "名",
        "last_name": "姓",
        "final_check": "入力した情報をご確認ください。\n登録を進めますか？"
    },
    "ko": {
        "intro": "가입 정보",
        "email": "이메일",
        "first_name": "이름",
        "last_name": "성",
        "final_check": "입력한 정보를 확인해 주세요.\n가입을 진행할까요?"
    }
}
PROMPT_CREATE_DOC: dict = {
    "en": {
        "intro": "💾 Starting registration of a new account.\nTo cancel, please press the cancel button above."
    },
    "ja": {
        "intro": "💾 新しいアカウント登録を開始します。\nキャンセルするには、上部のキャンセルボタンを押してください。"
    },
    "ko": {
        "intro": "💾 새 계정 등록을 시작합니다.\n취소하려면 위의 취소 버튼을 눌러주세요."
    }
}
PROMPT_DELETE_KRYPTOS: dict = {
    "en": {
        "intro": f"""️️⚠️ You are about to delete your {APP_NAME} account.
        
When deleting your {APP_NAME} account, the following data will be permanently deleted:

- {APP_NAME} account and settings information
- All account information stored in {APP_NAME}

Do you want to delete your {APP_NAME} account?""",
        "require_password": f"To delete your {APP_NAME} account, please enter your current {APP_NAME} account password."
    },
    "ja": {
        "intro": f"""️️⚠️ {APP_NAME}アカウントを削除しようとしています。
        
{APP_NAME}アカウントを削除すると、以下のデータが完全に削除されます。

- {APP_NAME}アカウントおよび設定情報
- {APP_NAME}に保存されているすべてのアカウント情報

{APP_NAME}アカウントを削除しますか？""",
        "require_password": f"{APP_NAME}アカウントを削除するには、現在の{APP_NAME}アカウントのパスワードを入力してください。"
    },
    "ko": {
        "intro": f"""️️⚠️ {APP_NAME} 계정 삭제를 진행합니다.
        
{APP_NAME} 계정 삭제 시, 아래의 자료가 즉시 파기됩니다.

- {APP_NAME} 계정 및 설정 정보
- {APP_NAME}에 저장한 모든 계정 정보

{APP_NAME} 계정을 삭제하시겠습니까?""",
        "require_password": f"{APP_NAME} 계정을 삭제합니다.\n현재 {APP_NAME} 계정 비밀번호를 입력해주세요."
    }
}
PROMPT_DOCS: dict = {
    "en": {
        "intro": "🗃️ Starting account management operations.\nWhat would you like to do?"
    },
    "ja": {
        "intro": "🗃️ アカウント管理操作を開始します。\n何を行いますか？"
    },
    "ko": {
        "intro": "🗃️ 계정 관리 작업을 시작합니다.\n어떤 작업을 진행할까요?"
    }
}
PROMPT_DOCS_DESCRIPTION: dict = {
    "en": {
        "intro": "✍️ Please enter a description for the account.\n",
        "guide": "Add a description to help with account searches.",
        "placeholder": "Enter account description"
    },
    "ja": {
        "intro": "✍️ アカウントの説明を入力してください。\n",
        "guide": "アカウント検索に役立つ説明を追加してください。",
        "placeholder": "アカウントの説明を入力"
    },
    "ko": {
        "intro": "✍️ 계정의 설명을 입력해주세요.\n",
        "guide": "계정 검색을 위한 설명을 추가해주세요.",
        "placeholder": "계정에 대한 설명 입력"
    }
}
PROMPT_DOC_NEW_PASSWORD: dict = {
    "en": {
        "intro": "✍️ Please enter the new password to register for this account.",
        "placeholder": "New Password: "
    },
    "ja": {
        "intro": "✍️ このアカウントに登録する新しいパスワードを入力してください。",
        "placeholder": "新しいパスワード: "
    },
    "ko": {
        "intro": "✍️ 이 계정에 등록할 새 비밀번호를 입력해주세요.",
        "placeholder": "새 비밀번호: "
    }
}
PROMPT_DOC_PASSWORD: dict = {
    "en": {
        "intro": "✍️ Please enter the password for the account.\n",
        "guide": "Please enter the existing password of the account registered on the site.",
        "placeholder": "Enter account password:"
    },
    "ja": {
        "intro": "✍️ アカウントのパスワードを入力してください。\n",
        "guide": "サイトに登録された既存のアカウントのパスワードを入力してください。",
        "placeholder": "アカウントパスワードを入力："
    },
    "ko": {
        "intro": "✍️ 계정의 비밀번호를 입력해주세요.\n",
        "guide": "사이트에 등록한 기존 계정의 비밀번호를 입력해주세요.",
        "placeholder": "등록 계정 비밀번호 입력:"
    }
}
PROMPT_DOC_PROTOCOL: dict = {
    "en": {
        "intro": "✍️ Please select the type of protocol for the site.\n",
        "guide": "Select the site protocol for the registered account. For general websites, choose HTTPS."
    },
    "ja": {
        "intro": "✍️ サイトのプロトコルの種類を選択してください。\n",
        "guide": "登録するアカウントのサイトプロトコルを選択してください。\n通常のウェブは HTTPS を選択してください。"
    },
    "ko": {
        "intro": "✍️ 사이트의 프로토콜 종류를 선택해 주세요.\n",
        "guide": "등록 계정의 사이트 프로토콜은 선택해주세요. \n일반 웹은 HTTPS를 선택해주세요."
    }
}
PROMPT_DOC_USERNAME: dict = {
    "en": {
        "intro": "✍️ Please enter the account ID or username.\n",
        "guide": "Enter the account ID or username registered with the site.",
        "placeholder": "Enter registered account ID or username"
    },
    "ja": {
        "intro": "✍️ アカウントIDまたはユーザー名を入力してください。\n",
        "guide": "サイトに登録されているアカウントIDまたはユーザー名を入力してください。",
        "placeholder": "登録済みのアカウントIDまたはユーザー名を入力"
    },
    "ko": {
        "intro": "✍️ 계정 ID 또는 사용자명을 입력해주세요.\n",
        "guide": "사이트에 등록한 계정 ID 또는 사용자명 등을 입력해주세요.",
        "placeholder": "등록 계정 ID 또는 사용명 "
    }
}
PROMPT_DOC_SITE: dict = {
    "en": {
        "fail": "❌ The input is not in a valid URL format.",
        "intro": "✍️ Please enter the website address for the account.\n",
        "guide": "Enter the URL for the account's website. Exclude protocols like 'http://'.\nFor example, if registering a Yahoo account, enter:\n- www.yahoo.com or\n- yahoo.com",
        "placeholder": "e.g., www.google.com"
    },
    "ja": {
        "fail": "❌ 入力が有効なURL形式ではありません。",
        "intro": "✍️ アカウントのサイトアドレスを入力してください。\n",
        "guide": "アカウントのサイトアドレスを入力してください。\n「http://」などのプロトコルは除外してください。\n例：Yahooアカウントを登録する場合、\n- www.yahoo.com または\n- yahoo.com",
        "placeholder": "例：www.google.com"
    },
    "ko": {
        "fail": "❌ URL 형식이 아닙니다.",
        "intro": "✍️ 계정의 사이트 주소를 입력해주세요.\n",
        "guide": "URL 주소는 등록할 계정의 사이트 주소를 입력해 주세요.\n'http://' 등의 프로토콜은 제외하시기 바랍니다.\n예) 야후 계정 등록 시 사이트 주소는, \n\n-  www.yahoo.com 또는\n-  yahoo.com",
        "placeholder": "예: www.google.com"
    }
}
PROMPT_EMAIL: dict = {
    "en": {
        "intro": "📧 Enter your email address.",
        "placeholder": "Email Address: ",
        "add_detail": """

Please enter your correct email address.
It would be used to get an activation code.""",
        "invalid": "❌ Not an email format.",
    },
    "ko": {
        "intro": "📧 Email 주소를 입력하세요.",
        "placeholder": "Email 주소: ",
        "add_detail": """

사용 중인 이메일 주소를 정확히 입력해주세요.
계정 활성화 코드가 메일로 발송됩니다.""",
        "invalid": "❌ Email 형식이 아닙니다.",
    },
    "ja": {
        "intro": "📧 メールを入力してください。.",
        "placeholder": "メールのアドレス: ",
        "add_detail": """

使用中の正しいメールのアドレスを入力してください。
アカウントの活性化コードをメールにてんそうします。""",
        "invalid": "❌ メールの形式じゃありません。",
    }

}
PROMPT_EDIT_LANGUAGE: dict = {
    "en": {
        "intro": "🌐 Please select the language you want to set from the buttons below."
    },
    "ja": {
        "intro": "🌐 設定したい言語を下のボタンから選択してください。"
    },
    "ko": {
        "intro": "🌐 설정하려는 언어를 아래의 버튼에서 선택해주세요."
    }
}
PROMPT_EDIT_MAX_ACCESS: dict = {
    "en": {
        "intro": "🔐 Changing the maximum login attempt limit.",
        "guide": "✍️ Enter a number between 3 and 5.\nTo cancel, please press the cancel button above.",
        "placeholder": "Max Access Try in Number:",
        "invalid_value": "❌ The input must be a number between 3 and 5."
    },
    "ja": {
        "intro": "🔐 最大ログイン試行回数を変更します。",
        "guide": "✍️ 3から5の間の数字を入力してください。\nキャンセルするには、上のキャンセルボタンを押してください。",
        "placeholder": "最大ログイン試行回数: ",
        "invalid_value": "❌ 入力値は3から5の間の数字である必要があります。"
    },
    "ko": {
        "intro": "🔐 최대 로그인 시도 횟수를 변경합니다.",
        "guide": "✍️ 3 ~ 5 사이 숫자를 입력해 주세요.\n취소하려면 위의 취소 버튼을 눌러주세요.",
        "placeholder": "최대 로그인 시도 횟수: ",
        "invalid_value": "❌  입력값은 3 ~ 5 사이 숫자입니다."
    }
}
PROMPT_EDIT_NAME: dict = {
    "en": {
        "intro": f"🪪 Modify the name registered with your {APP_NAME} account.",
        "first_name": "✍️ Please enter the first name you want to change in the input field.\nTo cancel, please press the cancel button above.",
        "last_name": "✍️ Please enter the last name you want to change in the input field.\nTo cancel, please press the cancel button above.",
        "placeholder": "At least one characters are required.",
        "edit_last_name_question": "Would you also like to edit your last name?",
        "edit_first_name_question": "Would you also like to edit your first name?"
    },
    "ja": {
        "intro": f"🪪 {APP_NAME}アカウントに登録された名前を修正します。",
        "first_name": "✍️ 変更する下の名前を入力欄に入力してください。\nキャンセルするには、上のキャンセルボタンを押してください。",
        "last_name": "✍️ 変更する名字を入力欄に入力してください。キャンセルするには、上のキャンセルボタンを押してください。",
        "placeholder": "1文字以上入力が必要です。",
        "edit_last_name_question": "名字も修正しますか？",
        "edit_first_name_question": "下の名前も修正しますか？"
    },
    "ko": {
        "intro": f"🪪 {APP_NAME} 계정에 등록한 이름을 수정합니다.",
        "first_name": "✍️ 변경할 이름을 입력창에 입력해주세요.\n취소하려면 위의 취소 버튼을 눌러주세요.",
        "last_name": "✍️ 변경할 성을 입력창에 입력해주세요.\n취소하려면 위의 취소 버튼을 눌러주세요.",
        "placeholder": "한 자리 이상 문자 입력 필요.",
        "edit_last_name_question": "성도 수정할까요?",
        "edit_first_name_question": "이름도 수정할까요?"
    }
}
PROMPT_EDIT_PASSWORD: dict = {
    "en": {
        "intro": f"🔑 Change your {APP_NAME} password."
    },
    "ja": {
        "intro": f"🔑 {APP_NAME}のパスワードを変更します。"
    },
    "ko": {
        "intro": f"🔑 {APP_NAME} 비밀번호를 변경합니다."
    }
}
PROMPT_EDIT_VISIBILITY: dict = {
    "en": {
        "intro": "*️⃣  Configuring password visibility. \nYou can hide your password with asterisk when you call your account information.",
        "guide": "✍️  Write down the visibility percentaget betweeb 20 ~ 80\nTo cancel, please press the cancel button above.",
        "placeholder": "Password Visibility: ",
        "invalid_value": "❌ Password visibility must be a number between 20 and 80."
    },
    "ja": {
        "intro": "*️⃣ パスワードの可視性を設定しています。\nアカウント情報を呼び出す際に、パスワードをアスタリスクで隠すことができます。",
        "guide": "✍️ 20～80の範囲で可視性の割合を記入してください。\nキャンセルするには、上のキャンセルボタンを押してください。",
        "placeholder": "パスワードの可視性: 20～80の範囲で数字を入力してください:",
        "invalid_value": "❌ パスワードの可視性は20～80の範囲の数字でなければなりません。"
    },
    "ko": {
        "intro": "*️⃣ 비밀번호 노출도를 설정합니다.\n계정 정보를 호출할 때 비밀번호를 별표로 숨길 수 있습니다.",
        "guide": "✍️ 20 ~ 80 사이의 노출도를 입력해주세요.\n취소하려면 위의 취소 버튼을 눌러주세요.",
        "placeholder": "비밀번호 노출도: 20 ~ 80 숫자 입력:",
        "invalid_value": "❌ 비밀번호 노출도 값은 20 ~ 80 사이 숫자만 입력 가능합니다."
    }
}
PROMPT_LICENSE: dict = {
    "en": {
        "continue": "To continue, please click the 'Skip' button.",
        "intro": "📜 Proceed with license tasks. Please select one of the options below.",
        "invalid": "❌ The license file is invalid. Please check it again.",
        "license_expire": "License Expiration Date",
        "license_issue": "License Issuance Date",
        "max_number_account": "Maximum Number of Registrable Accounts",
        "no_license": "🤔 There is no license registered yet.",
        "register_intro": "📜 Please upload the license file.\nClick the 📎 attachment button at the bottom of the input field -> then select the file button to proceed.",
        "show_intro": "✅ The registered license information is as follows."
    },
    "ja": {
        "continue": "続行するには「スキップ」ボタンをクリックしてください。",
        "intro": "📜 ライセンスの作業を進めます。以下のオプションから1つ選択してください。",
        "invalid": "❌ 無効なライセンスファイルです。再度ご確認ください。",
        "license_expire": "ライセンスの有効期限",
        "license_issue": "ライセンス発行日",
        "max_number_account": "登録可能な最大アカウント数",
        "no_license": "🤔 登録されたライセンスがありません。",
        "register_intro": "📜 ライセンスファイルをアップロードしてください。\n入力欄下部の 📎 添付ボタンをクリックして、ファイルを選択して進めてください。",
        "show_intro": "✅ 登録されたライセンス情報は以下の通りです。"
    },
    "ko": {
        "continue": "계속하려면 '건너뛰기' 버튼을 클릭해 주세요.",
        "intro": "📜 라이센스 작업을 진행합니다. 아래의 항목 중 하나를 선택해주세요.",
        "invalid": "❌ 유효하지 않은 라이센스 파일입니다. 다시 확인해주세요.",
        "license_expire": "라이센스 만료일",
        "license_issue": "라이센스 발급일",
        "max_number_account": "등록 가능 최대 계정 수",
        "no_license": "🤔 등록된 라이센스가 없습니다.",
        "register_intro": "⬆️ 라이센스 파일을 업로드 해 주세요.\n입력창 하단의 📎 첨부 및 파일 버튼을 클릭하여 진행해주세요.",
        "show_intro": "✅ 등록된 라이센스 정보는 아래와 같습니다."
    }
}
PROMPT_CONNECTION_ERROR: dict = {
    "en": {
        "api_conn": "🚨 Unable to connect to the API server.\nPlease try again later.",
        "db_conn": "🚨 Unable to connect to the database server.\nPlease try again later."
    },
    "ja": {
        "api_conn": "🚨 APIサーバーに接続できません。\nしばらくしてから再試行してください。",
        "db_conn": "🚨 データベースサーバーに接続できません。\nしばらくしてから再試行してください。"
    },
    "ko": {
        "api_conn": "🚨 API 서버에 연결할 수 없습니다.\n잠시 후 다시 시도해 주세요.",
        "db_conn": "🚨 DB 서버에 연결할 수 없습니다.\n잠시 후 다시 시도해 주세요."
    }
}
PROMPT_INVALID_USAGE: dict = {
    "en": {
        "error": "⛔ Invalid usage.\n\nPlease follow the guide.\n\nIf the issue persists, click the menu button in the bottom left -> 'main' to restart."
    },
    "ja": {
        "error": "⛔ 無効な操作です。\n\nガイドに従って進めてください。\n\n動作しない場合は、左下のメニューボタン -> 'main' をクリックして再起動してください。"
    },
    "ko": {
        "error": "⛔ 잘못된 접근입니다.\n\n가이드를 따라 진행해주세요.\n\n계속 동작하지 않는 경우, 좌측 하단 메뉴 버튼 -> 'main'을 눌러 다시 시작해주세요."
    }
}
PROMPT_SEARCH_DOCS: dict = {
    "en": {
        "intro": "🔍 Starting the account search.\nWhat information are you looking for?",
        "intro_description": "Search registered accounts by description.\nTo cancel, please press the cancel button above.",
        "intro_url": "Search registered accounts by site name.\nTo cancel, please press the cancel button above."
    },
    "ja": {
        "intro": "🔍 登録アカウントの検索を開始します。\nどの情報を検索しますか？",
        "intro_description": "説明（Description）で登録アカウントを検索します。\nキャンセルするには、上部のキャンセルボタンを押してください。",
        "intro_url": "サイト名で登録アカウントを検索します。\nキャンセルするには、上部のキャンセルボタンを押してください。"
    },
    "ko": {
        "intro": "🔍 등록 계정 검색을 시작합니다.\n어떤 정보를 검색할까요?",
        "intro_description": "등록 계정을 설명(Description)으로 검색합니다.\n취소하려면 위의 취소 버튼을 눌러주세요.",
        "intro_url": "등록 계정을 사이트 이름으로 검색합니다.\n취소하려면 위의 취소 버튼을 눌러주세요."
    }
}
PROMPT_SETTING: dict = {
    "en": {
        "intro": f"⚙️ Starting {APP_NAME} setting.\nWhat action would you like to take?",
        "show_intro": "⚙️ The current settings are as follows.",
        "edit_question": "⚙️ Would you like to proceed with changing the settings?",

        "email": "Email",
        "first_name": "First Name",
        "last_name": "Last Name",
        "language": "Language",
        "last_signin_datetime": "Last Signin",
        "last_signout_datetime": "Last Signout",
        "last_updated_datetime": "Last Updated",
        "max_access_try": "Maximum Login Attempts",
        "registered_datetime": "Registration Date",
        "visibility": "Password Visibility",
    },
    "ja": {
        "intro": f"⚙️ {APP_NAME}の設定を始めます。\nどの操作を行いますか？",
        "show_intro": "⚙️ 現在の設定は以下のとおりです。",
        "edit_question": "⚙️ 設定変更を進めますか？",

        "email": "メールアドレス",
        "first_name": "名",
        "last_name": "姓",
        "language": "言語",
        "last_signin_datetime": "最終ログイン",
        "last_signout_datetime": "最終ログアウト",
        "last_updated_datetime": "最終更新日",
        "max_access_try": "最大ログイン試行回数",
        "registered_datetime": "登録日",
        "visibility": "パスワードの可視性"
    },
    "ko": {
        "intro": f"⚙️ {APP_NAME} 설정을 시작합니다.\n어떤 작업을 진행할까요?",
        "show_intro": "⚙️ 현재 설정은 아래와 같습니다.",
        "edit_question": "⚙️ 설정 변경을 진행하시겠습니까?",

        "email": "이메일",
        "first_name": "이름",
        "last_name": "성",
        "language": "언어",
        "last_signin_datetime": "마지막 로그인",
        "last_signout_datetime": "마지막 로그아웃",
        "last_updated_datetime": "마지막 정보 수정일",
        "max_access_try": "최대 로그인 시도 횟수",
        "registered_datetime": "가입일",
        "visibility": "비밀번호 노출도",
    }

}
PROMPT_START: dict =  {
        "en": {
            "intro": "🫡 Hello '{}',\n",
            "serve_member": "What can I do you for?",
            "welcome": f"""
Before use {APP_NAME}, you should select sign in or sign up.
Please select one button you want to do.""",
            "activate_warning": "⚠️ Your account is not activated yet.\nStarting account activation."
        },
        "ja": {
            "intro": "🫡 こんにちは、’{}’さん。\n",
            "serve_member": "何を手伝っていたしますか？",
            "welcome":  f"""
{APP_NAME}を始めるために、ログインまたメンバー登録が秘強です。
次のバトンの中で一つ選んでください。""",
        "activate_warning": "⚠️ アカウントはまだ有効化されていません。\nアカウントの有効化を開始します。"
        },
        "ko": {
            "intro": "🫡 안녕하세요、’{}’ 님.\n",
            "serve_member": "무엇을 도와드릴까요?",
            "welcome": f"""
{APP_NAME}를 시작하기 위해 로그인 또는 회원가입이 필요합니다.
아래의 버튼 중 하나를 선택해 주세요.""",
        "activate_warning": "⚠️ 계정이 아직 활성화되지 않았습니다.\n계정 활성화를 시작합니다."
        }
}
PROMPT_SIGNIN: dict = {
    "en": {
        "intro": "➡️ Starting the signin process."
    },
    "ja": {
        "intro": "➡️ ログインを開始します。"
    },
    "ko": {
        "intro": "➡️ 로그인을 시작합니다."
    }
}
PROMPT_SIGNUP: dict = {
    "en": {
        "intro": "📝 Starting the signup process",
    },
    "ja": {
        "intro": "📝 メンバー登録を開始します"
    },
    "ko": {
        "intro": "📝 회원가입을 시작합니다."
    }
}
PROMPT_PASSWORD: dict = {
    "en": {
        "intro": "🔑 Enter your password.",
        "add_detail": """
Your password must include:
- At least 8 characters.
- At least one lowercase letter.
- At least one uppercase letter.
- At least one number.
- At least one special character.""",
        "change_pw": f"🔑 Please enter your current {APP_NAME} account password.",
        "invalid_length": "❌ The password must be at least 8 characters long.\n",
        "invalid_upper": "❌ The password must contain at least one uppercase letter.\n",
        "invalid_lower": "❌ The password must contain at least one lowercase letter.\n",
        "invalid_special": "❌ The password must contain at least one special character.\n",
        "invalid_digit": "❌ The password must contain at least one digit.\n",
        "new_password_intro": "🆕 Please enter the new password you want to set.\n",
        "place_holder": "Password: "
    },
    "ja": {
        "intro": "🔑 パスワードを入力してください。",
        "add_detail": """
パスワードには以下が含まれている必要があります:
- 最低8文字以上。
- 少なくとも1つの小文字を含む。
- 少なくとも1つの大文字を含む。
- 少なくとも1つの数字を含む。
- 少なくとも1つの特殊文字を含む。""",
        "change_pw": f"🔑 現在の{APP_NAME}アカウントのパスワードを入力してください。",
        "invalid_length": "❌ パスワードは最低8文字以上である必要があります。\n",
        "invalid_upper": "❌ パスワードは少なくとも1つの大文字を含む必要があります。\n",
        "invalid_lower": "❌ パスワードは少なくとも1つの小文字を含む必要があります。\n",
        "invalid_special": "❌ パスワードは少なくとも1つの特殊文字を含む必要があります。\n",
        "invalid_digit": "❌ パスワードは少なくとも1つの数字を含む必要があります。\n",
        "new_password_intro": "🆕 新しいパスワードを入力してください。\n",
        "place_holder": "パスワード: "
    },
    "ko": {
        "intro": "🔑 비밀번호를 입력하세요.",
        "add_detail": """
비밀번호는 다음을 포함해야 합니다:
- 최소 8자 이상.
- 하나의 소문자 포함.
- 하나의 대문자 포함.
- 하나의 숫자 포함.
- 하나의 특수 문자 포함.""",
        "change_pw": f"🔑 현재 {APP_NAME} 계정의 비밀번호를 입력해주세요",
        "invalid_length": "❌ 비밀번호는 최소 8자 이상이어야 합니다.\n",
        "invalid_upper": "❌ 비밀번호는 적어도 하나의 대문자를 포함해야 합니다.\n",
        "invalid_lower": "❌ 비밀번호는 적어도 하나의 소문자를 포함해야 합니다.\n",
        "invalid_special": "❌ 비밀번호는 적어도 하나의 특수 문자를 포함해야 합니다.\n",
        "invalid_digit": "❌ 비밀번호는 적어도 하나의 숫자를 포함해야 합니다.\n",
        "new_password_intro": "🆕 새로 지정할 비밀번호를 입력해주세요.\n",
        "place_holder": "비밀번호: "
    }
}
PROMPT_UPDATE_DOC: dict = {
    "en": {
        "intro": "📝 Starting the update process for the selected account.\nPlease select the information to update."
    },
    "ja": {
        "intro": "📝 選択したアカウントの修正作業を開始します。\n修正する情報を選択してください。"
    },
    "ko": {
        "intro": "📝 선택한 계정의 수정 작업을 시작합니다.\n수정할 정보를 선택해 주세요."
    }
}
PROMPT_BUTTON: dict = {
    "en": {
        "yes_btn": "✅ Yes",
        "no_btn": "❌ No",
        "account_btn": "👤 Manage Accounts",
        "cancel_btn": "🛇 Cancel",
        "create_new_doc": "🆕 Register New Account",
        "delete_kryptos_btn": f"Delete {APP_NAME}",
        "delete_doc_btn": "🗑️ Delete This Account",
        "edit_max_access_btn": "Change Login Attempts",
        "edit_first_name_btn": "Change First Name",
        "edit_last_name_btn": "Change Last Name",
        "edit_language_btn": "Change Language",
        "edit_name_btn": "Change Name",
        "edit_password_btn": "Change Password",
        "edit_visibility_btn": "Change Account Visibility",
        "get_settings_btn": "Show Settings",
        "home_btn": "Home Menu",
        "license_btn": "License",
        "mgmt_btn": f"Configure {APP_NAME}",
        "pt_https_btn": "Web (HTTPS)",
        "pt_http_btn": "Unencrypted Web (HTTP)",
        "pt_ftp_btn": "File Transfer (FTP)",
        "pt_ssh_btn": "Secure Shell (SSH)",
        "pt_jdbc_btn": "JDBC",
        "pt_srv_btn": "SRV",
        "register_license_btn": "Register License",
        "show_license_btn": "Check License",
        "show_settings_btn": "Show Settings",
        "send_code_btn": "Send Code",
        "search_docs": "🔍 Search Registered Accounts",
        "search_docs_site": "Search by Site Name",
        "search_docs_description": "Search by Description",
        "setting_btn": "⚙️ Settings",
        "signin_btn": "➡️ Sign In",
        "signup_btn": "📝 Sign Up",
        "signout_btn": "⬅️ Sign Out",
        "skip_btn": "⏭️ Skip",
        "statistics_docs": "📊 Account Statistics",
        "update_description_btn": "Update Description",
        "update_password_btn": "Password",
        "update_protocol_btn": "Protocol",
        "update_site_btn": "Site",
        "update_username_btn": "ID / Username",
        "update_doc_btn": "🔄 Update This Account"
    },
    "ja": {
        "yes_btn": "✅ はい",
        "no_btn": "❌ いいえ",
        "account_btn": "👤 アカウント管理",
        "cancel_btn": "🛇 キャンセル",
        "create_new_doc": "🆕 新しいアカウントを登録",
        "delete_kryptos_btn": f"{APP_NAME}を削除",
        "delete_doc_btn": "🗑️ このアカウントを削除",
        "edit_max_access_btn": "ログイン試行回数を変更",
        "edit_first_name_btn": "名（First Name）を変更",
        "edit_last_name_btn": "姓（Last Name）を変更",
        "edit_language_btn": "言語を変更",
        "edit_name_btn": "名前を変更",
        "edit_password_btn": "パスワードを変更",
        "edit_visibility_btn": "アカウントの公開範囲を変更",
        "get_license_btn": "ライセンス確認",
        "home_btn": "ホームメニュー",
        "license_btn": "ライセンス",
        "mgmt_btn": f"{APP_NAME}を設定",
        "pt_https_btn": "Web（HTTPS）",
        "pt_http_btn": "暗号化なし Web（HTTP）",
        "pt_ftp_btn": "ファイル転送（FTP）",
        "pt_ssh_btn": "セキュアシェル（SSH）",
        "pt_jdbc_btn": "JDBC",
        "pt_srv_btn": "SRV",
        "register_license_btn": "ライセンス登録",
        "send_code_btn": "コードを送信",
        "search_docs": "🔍 登録アカウントを検索",
        "search_docs_site": "サイト名で検索",
        "search_docs_description": "説明で検索",
        "show_settings_btn": "設定を表示",
        "setting_btn": "⚙️ 設定",
        "signin_btn": "➡️ サインイン",
        "signup_btn": "📝 サインアップ",
        "signout_btn": "⬅️ サインアウト",
        "skip_btn": "⏭️ スキップ",
        "statistics_docs": "📊 アカウント統計",
        "update_description_btn": "説明を更新",
        "update_password_btn": "パスワード",
        "update_protocol_btn": "プロトコル",
        "update_site_btn": "サイト",
        "update_username_btn": "ID / ユーザー名",
        "update_doc_btn": "🔄 このアカウントを更新"
    },
    "ko": {
        "yes_btn": "✅ 네",
        "no_btn": "❌ 아니오",
        "account_btn": "👤 계정 관리",
        "cancel_btn": "🛇 취소",
        "create_new_doc": "🆕 새 계정 등록",
        "delete_kryptos_btn": f"{APP_NAME} 삭제",
        "delete_doc_btn": "🗑️ 이 계정 삭제",
        "edit_max_access_btn": "로그인 시도 횟수 변경",
        "edit_first_name_btn": "이름(First name)변경",
        "edit_last_name_btn": "성(Last name) 변경",
        "edit_language_btn": "언어 변경",
        "edit_name_btn": "이름 변경",
        "edit_password_btn": "비밀번호 변경",
        "edit_visibility_btn": "계정 노출도 변경",
        "get_license_btn": "라이센스 확인",
        "home_btn": "홈 메뉴",
        "license_btn": "라이센스",
        "mgmt_btn": f"{APP_NAME} 설정",
        "pt_https_btn": "일반 웹 (HTTPS)",
        "pt_http_btn": "비암호화 웹 (HTTP)",
        "pt_ftp_btn": "파일 전송 (FTP)",
        "pt_ssh_btn": "Secure Shell (SSH)",
        "pt_jdbc_btn": "JDBC",
        "pt_srv_btn": "SRV",
        "register_license_btn": "라이센스 등록",
        "send_code_btn": "코드 전송",
        "search_docs": "🔍 등록 계정 검색",
        "search_docs_site": "사이트명으로 검색",
        "search_docs_description": "설명으로 검색",
        "show_settings_btn": "설정 표시",
        "setting_btn": "⚙️ 설정",
        "signin_btn": "➡️ 로그인",
        "signup_btn": "📝 회원가입",
        "signout_btn": "⬅️ 로그아웃",
        "skip_btn": "⏭️ 건너뛰기",
        "statistics_docs": "📊 등록 계정 통계",
        "update_description_btn": "등록 설명",
        "update_password_btn": "비밀번호",
        "update_protocol_btn": "프로토콜",
        "update_site_btn": "사이트",
        "update_username_btn": "ID / 사용자명",
        "update_doc_btn": "🔄 이 계정 정보 수정"
    }
}