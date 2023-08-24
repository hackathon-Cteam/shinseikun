async function requestPost(url, data) {
  let responseData = null;
  await fetch(url,
    { method: 'POST', headers : { 'Content-type' : 'application/json; charset=utf-8' }, body : JSON.stringify(data) }
  ).then((response) => {
    if (!response.ok) {
      return Promise.reject(new Error(`status code: ${response.status}`));
    }
    return response.json();
  }).then((data) => {
    responseData = data;
  });
  return responseData;
}

async function changeReservationStatusRequest(action, reserinfoId, buttonId, j) {
  try {
    await requestPost(`/${action}-reservation`, { reserinfoId });
    let statusbtn = document.getElementById(buttonId).value;
    let tableA = document.getElementById("sort_table");
    let c = j+1;
    console.log(c);
    tableA.rows[c].cells[5].innerText = statusbtn;
  } catch (error) {
    console.log(error.message);
    alert(`操作が正常に終了できませんでした。\n一覧のステータスを確認してください。`);
  }
}

/*テーブル1のステータス選択ボタン（受領ボタン）*/
function statusbtn1() {
  const statuscheck = document.getElementsByName("statuscheck");
  for (let j = 0; j < statuscheck.length; j++) {
    if (statuscheck[j].checked) {
      changeReservationStatusRequest('received', statuscheck[j].getAttribute('data-reserinfo-id'), 'statusbtn1', j);
    }
  }
}

/*テーブル1のステータス選択ボタン（承認ボタン）*/
function statusbtn2() {
  const statuscheck = document.getElementsByName("statuscheck");
  for (let j = 0; j < statuscheck.length; j++) {
    if (statuscheck[j].checked) {
      changeReservationStatusRequest('approval', statuscheck[j].getAttribute('data-reserinfo-id'), 'statusbtn2', j);
    }
  }
}

/*テーブル1のステータス選択ボタン（否認ボタン）*/
function statusbtn3() {
  const statuscheck = document.getElementsByName("statuscheck");
  for (let j = 0; j < statuscheck.length; j++) {
    if (statuscheck[j].checked) {
      changeReservationStatusRequest('cancel', statuscheck[j].getAttribute('data-reserinfo-id'), 'statusbtn3', j);
    }
  }
}

window.addEventListener('load', () => {
  //施設名の絞り込み検索機能の登録処理（別途記載）を実行
  registerSortFacilityEvent1();
});

/**
 * 検索機能1  施設名の絞り込み検索機能の登録処理
 */
function registerSortFacilityEvent1() {
  //検索ボタンを取得
  const sortButton1 = document.getElementById("sortButton1");
  //検索ボタンクリック時
  sortButton1.addEventListener("click", function() {
    sortFacility1();    //施設名の絞り込み検索処理（別途記載）を実行
    console.log("検索の実行");    //挙動確認用
  });
}

/**
 * 施設名の絞り込み検索処理
 */
function sortFacility1() {
  const sortKeywordValue1 = document.getElementById("sortKeyword1").value.toUpperCase();    //検索フォームに入力されたキーワードをの値を取得（大文字に揃える）
  const facilityList1 = document.getElementsByClassName("facilityList1");    //選択肢（選択ボタン＋施設名）の要素を取得
  const facilityName1 = document.getElementsByClassName("facilityName1");    //施設名の要素を取得
  
  for (i = 0; i < facilityList1.length; i++) {    //選択肢の要素の個数分繰り返し
    const facilityNameValue1 = facilityName1[i].textContent;    //施設名の要素から値を抽出し変数に代入
    if (facilityNameValue1.toUpperCase().search(sortKeywordValue1) > -1) {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
      facilityList1[i].style.display = "";    //選択肢の要素を表示
    } else {
      facilityList1[i].style.display = "none";   //その他の場合は選択肢の要素を非表示
    }
  }
}

//テーブル1のソート機能
window.addEventListener('load', function () {
  let column_no = 0; //今回クリックされた列番号
  let column_no_prev = 0; //前回クリックされた列番号
  document.querySelectorAll('#sort_table th').forEach(elm => {
    elm.onclick = function () {
      column_no = this.cellIndex; //クリックされた列番号
      let table = this.parentNode.parentNode.parentNode;
      let sortType = 0; //0:数値 1:文字
      let sortArray = new Array; //クリックした列のデータを全て格納する配列
      for (let r = 1; r < table.rows.length; r++) {
        //行番号と値を配列に格納
        let column = new Object;
        column.row = table.rows[r];
        column.value = table.rows[r].cells[column_no].textContent;
        sortArray.push(column);
        //数値判定
        if (isNaN(Number(column.value))) {
          sortType = 1; //値が数値変換できなかった場合は文字列ソート
        }
      }
      if (sortType == 0) { //数値ソート
        if (column_no_prev == column_no) { //同じ列が2回クリックされた場合は降順ソート
          sortArray.sort(compareNumberDesc);
        } else {
          sortArray.sort(compareNumber);
        }
      } else { //文字列ソート
        if (column_no_prev == column_no) { //同じ列が2回クリックされた場合は降順ソート
          sortArray.sort(compareStringDesc);
        } else {
          sortArray.sort(compareString);
        }
      }
      //ソート後のTRオブジェクトを順番にtbodyへ追加（移動）
      let tbody = this.parentNode.parentNode;
      for (let i = 0; i < sortArray.length; i++) {
        tbody.appendChild(sortArray[i].row);
      }
      //昇順／降順ソート切り替えのために列番号を保存
      if (column_no_prev == column_no) {
        column_no_prev = -1; //降順ソート
      } else {
        column_no_prev = column_no;
      }
    };
  });
});

//数値ソート（昇順）
function compareNumber(a, b) {
  return a.value - b.value;
}

//数値ソート（降順）
function compareNumberDesc(a, b) {
  return b.value - a.value;
}

//文字列ソート（昇順）
function compareString(a, b) {
  if (a.value < b.value) {
    return -1;
  } else {
    return 1;
  }
}

//文字列ソート（降順）
function compareStringDesc(a, b) {
  if (a.value > b.value) {
    return -1;
  } else {
    return 1;
  }
}

//ステータスに合わせてセルに色をつける
/*function cellcolor() {
  const row = document.getElementsByClassName("facilityName").rows.item(0);    // 行の取得
  const cell = row.cells.item(-1);
  facilityNameValue = facilityName[i].textContent;    //施設名の要素から値を抽出し変数に代入
    if (facilityNameValue === "受領") {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
      facilityList1[i].style.display = "";    //選択肢の要素を表示
}

// 行の取得
var row = document.getElementById("tableId").rows.item(0);
// セルの取得
var cell = row.cells.item(-1);
// 背景色の変更
cell.style.backgroundColor = "#A52A2A";
*/

async function addChannelRequest(channelName) {
  try {
    const result = await requestPost('/add-channel', { channelName });
    const table = document.getElementById("table");
    // 行を行末に追加
    const row = table.insertRow(-1);
    //td分追加
    const cell1 = row.insertCell(-1);
    const cell2 = row.insertCell(-1);
    // セルの内容入力
    cell1.innerHTML = `<input type="checkbox" name="facility" data-channel-id="${result.channelId}">`;
    cell2.innerText = channelName;
  } catch (error) {
    console.log(error.message);
    alert('チャンネルが追加できませんでした');
  }
}

//チャンネル追加機能
function coladd() {
  addChannelRequest(document.getElementById("channelName").value);
}

async function deleteChannelRequest(channelId, facility) {
  try {
    await requestPost('/delete-channel', { channelId });
    facility.closest('tr').remove();
  } catch (error) {
    console.log(error.message);
    alert(`チャンネルが追加できませんでした`);
  }
}

//チャンネル削除機能
function deleatRow() {
  const facility = document.getElementsByName("facility");
  for (let i = 0; i < facility.length; i++) {
    if (facility[i].checked) {
      deleteChannelRequest(facility[i].getAttribute('data-channel-id'), facility[i]);
    }
  }
}

window.addEventListener('load', () => {
  //施設名の絞り込み検索機能の登録処理（別途記載）を実行
  registerSortFacilityEvent();
});

/**
 * 検索機能2  施設名の絞り込み検索機能の登録処理
 */
function registerSortFacilityEvent() {
  //検索ボタンを取得
  const sortButtonB = document.getElementById("sortButton");
  //検索ボタンクリック時
  sortButtonB.addEventListener("click", function() {
    sortFacility();    //施設名の絞り込み検索処理（別途記載）を実行
    console.log("検索の実行です。");    //挙動確認用
  });
}

/**
 * 施設名の絞り込み検索処理
 */
function sortFacility() {
  const sortKeywordValue = document.getElementById("sortKeyword").value.toUpperCase();    //検索フォームに入力されたキーワードをの値を取得（大文字に揃える）
  const facilityList = document.getElementsByClassName("facilityList");    //選択肢（選択ボタン＋施設名）の要素を取得
  const facilityName = document.getElementsByClassName("facilityName");    //施設名の要素を取得
  for (h = 0; h < facilityList.length; h++) {    //選択肢の要素の個数分繰り返し
    const facilityNameValue = facilityName[h].textContent;    //施設名の要素から値を抽出し変数に代入
    if (facilityNameValue.toUpperCase().search(sortKeywordValue) > -1) {    //施設名の値とキーワードの値が不一致でなければ（施設名の値は大文字に揃える）
      facilityList[h].style.display = "";    //選択肢の要素を表示
    } else {
      facilityList[h].style.display = "none";   //その他の場合は選択肢の要素を非表示
    }
  }
}
