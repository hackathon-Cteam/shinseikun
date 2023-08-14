// /**
//  * 入力エラーチェック
//  */
// function checkInput() {
//   if (
//       application_form.purpose.value == "" ||
//       application_form.name.value == "" ||
//       application_form.email.value == "" ||
//       application_form.phone.value == ""
//   ){
//       //上記条件に一致する場合
//       alert("空欄もしくは未選択の項目があります");    //エラーメッセージを出力
//       return false;    //送信ボタン本来の動作をキャンセルします
//   } else {
//       return true;    //送信ボタン本来の動作を実行します
//   }
// }

/**
 * 施設名の絞り込み検索
 */

function sortFacility() {
    const sortKeyword = document.getElementById("sortKeyword").value.toUpperCase();    //検索フォームに入力されたキーワードを取得（大文字に揃える）
    const facilityList = document.getElementsByClassName("facilityList");    //選択肢（選択ボタン＋施設名）を取得
    const facilityName = document.getElementsByClassName("facilityName");    //施設名を取得

      for (i = 0; i < facilityList.length; i++) {    //選択肢の個数分繰り返し
        value = facilityName[i].textContent;    //施設名の値を変数に代入
        if (value.toUpperCase().indexOf(sortKeyword) > -1) {    //施設名の値とキーワードが不一致でなければ（施設名は大文字に揃える）
          facilityList[i].style.display = "";    //選択肢を表示
        } else {
          facilityList[i].style.display = "none";   //その他の場合は選択肢を非表示
        }
      }
}