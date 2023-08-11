function check(){
  if (
      application_form.purpose.value == "" ||
      application_form.name.value == "" ||
      application_form.email.value == "" ||
      application_form.phone.value == ""
  ){
      //上記条件に一致する場合
      alert("空欄のある項目があります");    //エラーメッセージを出力
      return false;    //送信ボタン本来の動作をキャンセルします
  }else{
      return true;    //送信ボタン本来の動作を実行します
  }
}