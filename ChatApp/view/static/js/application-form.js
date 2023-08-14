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
 * ページ読み込み時の処理
 */

//検索ボタンとフォーム要素を取得
window.addEventListener('load', function() {
  const sortButton = document.getElementById("sortButton");
  const form = document.querySelector("#form");

    //検索ボタンクリック時の処理を定義
    sortButton.addEventListener("click", function() {
      sortFacility();    //施設名の絞り込み検索を実行
      console.log("検索の実行");    //挙動確認用
    })

    //フォーム送信時の処理を定義
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      console.log("モーダルの立ち上げ");    //挙動確認用
      //※モーダル立ち上げ処理を実装予定
    })
})



/**
 * 施設名の絞り込み検索機能
 */
function sortFacility() {
  const sortKeywordValue = document.getElementById("sortKeyword").value.toUpperCase();    //検索フォームに入力されたキーワードをの値を取得（大文字に揃える）
  const facilityList = document.getElementsByClassName("facilityList");    //選択肢（選択ボタン＋施設名）の要素を取得
  const facilityName = document.getElementsByClassName("facilityName");    //施設名の要素を取得

    for (i = 0; i < facilityList.length; i++) {    //選択肢の要素の個数分繰り返し
      facilityNameValue = facilityName[i].textContent;    //施設名の要素から値を抽出し変数に代入
      if (facilityNameValue.toUpperCase().indexOf(sortKeywordValue) > -1) {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
        facilityList[i].style.display = "";    //選択肢の要素を表示
      } else {
        facilityList[i].style.display = "none";   //その他の場合は選択肢の要素を非表示
      }
    }
}
