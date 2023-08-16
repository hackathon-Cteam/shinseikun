window.addEventListener('load', () => {
    //施設名の絞り込み検索機能の登録処理（別途記載）を実行
    registerSortFacilityEvent();
})

/**
 * 施設名の絞り込み検索機能の登録処理
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
 * 施設名の絞り込み検索処理
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
function compareNumber(a, b)
{
	return a.value - b.value;
}
//数値ソート（降順）
function compareNumberDesc(a, b)
{
	return b.value - a.value;
}
//文字列ソート（昇順）
function compareString(a, b) {
	if (a.value < b.value) {
		return -1;
	} else {
		return 1;
	}
	return 0;
}
//文字列ソート（降順）
function compareStringDesc(a, b) {
	if (a.value > b.value) {
		return -1;
	} else {
		return 1;
	}
	return 0;
}

//チャンネル追加機能
function coladd() {
	var table = document.getElementById("table");
	// 行を行末に追加
	var row = table.insertRow(-1);
	//td分追加
	var cell1 = row.insertCell(-1);
	var cell2 = row.insertCell(-1);
	// セルの内容入力
	cell1.innerHTML = '<input type="checkbox" name="facility" required>';
	cell2.innerHTML = 'この行を削除しますか？<input type="button" value="削除" id="coladd" onclick="coldel(this)">';
}
function coldel(obj) {
	// 削除ボタンを押下された行を取得
	tr = obj.parentNode.parentNode;
	// trのインデックスを取得して行を削除する
	tr.parentNode.deleteRow(tr.sectionRowIndex);
}

//チャンネル追加機能で入力したテキストを反映
/*
function butotnClick(){
	msg.innerText = 'お名前は' + channelName.value + 'さんですね';
  }
  
  let channelName = document.getElementById('channelName');
  let msg = document.getElementById('msg');
  
  let coladd = document.getElementById('coladd');
  coladd.addEventListener('click', butotnClick);
  */