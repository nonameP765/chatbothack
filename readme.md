# 허준봇

## 개요

> 자신의 체형을 알아볼 수 있는 서비스입니다.
https://pf.kakao.com/_yxoJnj

## 사용법


1. git clone "https://github.com/nonameP765/chatbothack.git"<br><br>
2. cd 클론된폴더<br><br>
3. mkdir .config_secret<br><br>
4. 아래와 같이 프로젝트 루트에 파일 생성<br><br>
 .config_secret<br>
┣━━━ settings_common.json<br>
┣━━━ settings_debug.json<br>
┗━━━ settings_deploy.json<br><br><pre>
settings_common.json<br><br><code>{
  "django": {
    "secret_key": 장고 KEY값,
    "database": DB정보
  }
}
</code><br>
settings_debug.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      테스트용 호스트
    ]
  }
}
</code><br>
settings_deploy.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      서빙용 호스트
    ]
  }
}
</code>
</pre>5. 마이그레이션 등등 설정...<br><br>
6. 디버깅용 옵션 --settings=chatbothack.settings.debug <br>
실서비스용 옵션 --settings=chatbothack.settings.deploy
<br><br>
*우분투 18.04를 기준으로 만들어졌습니다!