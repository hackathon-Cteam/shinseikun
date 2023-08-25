import requestPost from './common/request.js';
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
 * ページ読み込み時に実施する処理
 */
window.addEventListener('load', () => {
    //施設名の絞り込み検索機能の登録（別途記載）を実行
    registerSortFacilityEvent();
    //確認モーダルを立ち上げる機能の登録（別途記載）を実行
    registerCreateConfirmModalEvent();
    //確認モーダルを閉じる機能の登録（別途記載）を実行
    registerCloseConfirmModalEvent();
    //確認モーダルをsubmitした際の処理の登録（別途記載）を実行
    registerSubmitConfirmModalEvent();
    //日付選択ボックスの選択肢の生成（別途記載）を実行
    createDateSelectBoxOption();
})

/**
 * 施設名の絞り込み検索機能の登録
 */
function registerSortFacilityEvent() {
  //検索ボタンを取得
  const sortButton = document.getElementById("sortButton");
     //検索ボタンクリック時
     sortButton.addEventListener("click", function() {
      sortFacility();    //施設名の絞り込み検索処理（別途記載）を実行
      console.log("検索の実行");    //挙動確認用
    })
}

/**
 * 確認モーダルを立ち上げる機能の登録
 */
function registerCreateConfirmModalEvent() {
  //親画面のフォーム要素を取得
  const form = document.querySelector("#form");
  //確認モーダル要素を取得
  const confirmModal = document.getElementById('confirm-modal');
    //親画面のフォームのsubmit時
    form.addEventListener("submit", function(event) {
      event.preventDefault();    //親画面のフォームのsubmitを一旦キャンセル
      confirmModal.style.display = 'block';    //確認モーダルの立ち上げ
      showSubmitInfo();    //親画面に入力した情報を確認モーダルに表示する処理（別途記載）を実行
      console.log("確認モーダルの立ち上げ");    //挙動確認用
    })
}

/**
 * 確認モーダルを閉じる機能の登録
 */
function registerCloseConfirmModalEvent() {
  //確認モーダル要素を取得
  const confirmModal = document.getElementById('confirm-modal');
  //確認モーダルを閉じるボタンを取得
  const closeConfirmModalButton = document.getElementById('confirm-modal-close');
    // 閉じるボタンクリック時
    closeConfirmModalButton.addEventListener('click', function() {
      confirmModal.style.display = 'none';   //確認モーダルを閉じる
      console.log("確認モーダルを閉じる");    //挙動確認用
    })
}

/**
 * 確認モーダルをsubmitした際の処理の登録
 */
function registerSubmitConfirmModalEvent() {
  //親画面のフォーム要素を取得
  const form = document.querySelector("#form");
  //確認モーダルのフォーム要素を取得
  const confirmModalForm = document.querySelector("#confirm-modal-form");
    //確認モーダルのsubmit時
    confirmModalForm.addEventListener("submit", function(event) {
      event.preventDefault();    //確認モーダルのフォームのsubmitは行わない
      const channel = confirmModalForm.querySelector('#rsv-channel-confirm').innerText;
      const date = confirmModalForm.querySelector('#rsv-date-confirm').innerText;
      const time = confirmModalForm.querySelector('#rsv-time-confirm').innerText;
      let channelId;
      document.querySelectorAll('.facilityList input').forEach((radio) => {
        if (radio.checked) {
            channelId = radio.value
        }
      });
      requestPost('/post-message', { message: `${channel}の利用を以下の日程で申請しました。\n【利用日】 ${date}\n【時間帯】${time}`, channelId });
      form.submit()    //停止していた親画面のフォームのsubmitを実施
      console.log("親画面のフォームを送信しマイページへ遷移");    //挙動確認用
    })
}

/**
 * 施設名の絞り込み検索処理
 */
function sortFacility() {
  const sortKeywordValue = document.getElementById("sortKeyword").value.toUpperCase();    //検索フォームに入力されたキーワードをの値を取得（大文字に揃える）
  const facilityList = document.getElementsByClassName("facilityList");    //選択肢（選択ボタン＋施設名）の要素を取得
  const facilityName = document.getElementsByClassName("facilityName");    //施設名の要素を取得

    for (i = 0; i < facilityList.length; i++) {    //選択肢の要素の個数分繰り返し
      facilityNameValue = facilityName[i].textContent;    //施設名の要素から値を抽出し変数に代入
      if (facilityNameValue.toUpperCase().search(sortKeywordValue) > -1) {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
        facilityList[i].style.display = "";    //選択肢の要素を表示
      } else {
        facilityList[i].style.display = "none";   //その他の場合は選択肢の要素を非表示
      }
    }
}

/**
 * 親画面に入力した情報を確認モーダルに表示する処理
 */
function showSubmitInfo() {
  const year = document.getElementById("rsv-year").value;
  const month = document.getElementById("rsv-month").value;
  const day = document.getElementById("rsv-day").value;
  const startHour = document.getElementById("rsv-time-start-hour").value;
  const startMinute = document.getElementById("rsv-time-start-minute").value;
  const endHour = document.getElementById("rsv-time-end-hour").value;
  const endMinute = document.getElementById("rsv-time-end-minute").value;

  //ラジオボタンで選択されている要素の名前を取得
  const facilityName = document.getElementsByClassName("facilityName");
  const elements = document.getElementsByName('facility');
  let len = elements.length;
  let checkedValue = '';

    for (let i = 0; i < len; i++){
      if (elements.item(i).checked){
          checkedValue = facilityName[i].textContent;
      }
    }
    console.log(`ラジオボタンで選択されているのは「${checkedValue}」です`);    //挙動確認用

      //モーダル画面へ値を表示
      document.getElementById("rsv-channel-confirm").textContent = checkedValue;
      document.getElementById("rsv-date-confirm").textContent = `${year}年${month}月${day}日`;
      document.getElementById("rsv-time-confirm").textContent = `${startHour}:${startMinute}〜${endHour}:${endMinute}`;
}


/**
 * 日付選択ボックスの選択肢の生成
 */
function createDateSelectBoxOption() {
  // ライブラリ
  /**
   * 任意の年が閏年であるかをチェックする
   * @param {number} チェックしたい西暦年号
   * @return {boolean} 閏年であるかを示す真偽値
   */
  const isLeapYear = year => (year % 4 === 0) && (year % 100 !== 0) || (year % 400 === 0);

  /**
   * 任意の年の2月の日数を数える
   * @param {number} チェックしたい西暦年号
   * @return {number} その年の2月の日数
   */
  const countDatesOfFeb = year => isLeapYear(year) ? 29 : 28;

  /**
   * セレクトボックスの中にオプションを生成する
   * @param {string} セレクトボックスのDOMのid属性値
   * @param {number} オプションを生成する最初の数値
   * @param {number} オプションを生成する最後の数値
   * @param {number} 現在の日付にマッチする数値
   */
  const createOption = (id, startNum, endNum, current) => {
    const selectDom = document.getElementById(id);
    let optionDom = '';
    for (let i = startNum; i <= endNum; i++) {
        let option;
      if (i === current) {
        option = '<option value="' + i + '" selected>' + i + '</option>';
      } else {
        option = '<option value="' + i + '">' + i + '</option>';
      }
      optionDom += option;
    }
    selectDom.insertAdjacentHTML('beforeend', optionDom);
  }

  // DOM
  const yearBox = document.getElementById('rsv-year');
  const monthBox = document.getElementById('rsv-month');
  const dateBox = document.getElementById('rsv-day');

  // 日付データ
  const today = new Date();
  const thisYear = today.getFullYear();
  const thisMonth = today.getMonth() + 1;
  const thisDate = today.getDate();

  let datesOfYear= [31, countDatesOfFeb(thisYear), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  // イベント（選択肢の変更）
  monthBox.addEventListener('change', (e) => {
    dateBox.innerHTML = '';
    const selectedMonth = e.target.value;

    if (selectedMonth == thisMonth && yearBox.value == thisYear) {   //当月(かつ当年)への変更の場合の処理（ロード時の選択肢状態とする）
      monthBox.innerHTML = '';
      createOption('rsv-month', thisMonth, 12, thisMonth);
      createOption('rsv-day', thisDate, datesOfYear[thisMonth - 1], thisDate);
    } else {    //当月以外への変更の場合の処理
      createOption('rsv-day', 1, datesOfYear[selectedMonth - 1], 1);
    }
  });

  yearBox.addEventListener('change', e => {
    monthBox.innerHTML = '';
    dateBox.innerHTML = '';
    const updatedYear = e.target.value;
    datesOfYear = [31, countDatesOfFeb(updatedYear), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    if (updatedYear == thisYear) {    //当年への変更の場合の処理（ロード時の選択肢状態とする）
      createOption('rsv-month', thisMonth, 12, thisMonth);
      createOption('rsv-day', thisDate, datesOfYear[thisMonth - 1], thisDate);
    } else {    //当年以外への変更の場合の処理
      createOption('rsv-month', 1, 12, 1);
      createOption('rsv-day', 1, datesOfYear[0], 1);
    }
  });

  // ロード時の選択肢
  createOption('rsv-year', thisYear, thisYear + 1, thisYear);  // 最小値＝当年、最大値＝翌年、デフォルト＝当年
  createOption('rsv-month', thisMonth, 12, thisMonth);  // 最小値＝当月、最大値＝12、デフォルト＝当月
  createOption('rsv-day', thisDate, datesOfYear[thisMonth - 1], thisDate);    // 最小値＝当月、最大値＝その月により設定、デフォルト＝当日
}