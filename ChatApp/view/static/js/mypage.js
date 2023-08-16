//クリックした時の処理
document.querySelector('#modal-button').addEventListener('click', openModalWindow);

//モーダルウィンドウを表示する
function openModalWindow(){

  //モーダルを生成する→新しいタグを生成
  const modalElement = document.createElement('div');
  
  // 作ったdivの中にcss→modalを付与する
  modalElement.classList.add('modal');

  //モーダルウィンドウの中身を作る
  //新しいdivタグを生成する
  const innerElement = document.createElement('div');
  //作ったdivの中にcss→innerを付与する
  innerElement.classList.add('inner');
  innerElement.innerHTML =
  `<p>モーダルの中身です</p>
  <p>テキストや画像も入るよ</p>`
  ;
  //モーダルの中身に要素を配置する
  modalElement.appendChild(innerElement);
  //body要素にモーダルを配置する
  document.body.appendChild(modalElement);


  //中身をクリックしたらモーダルウインドウを削除する
  innerElement.addEventListener('click',() => {
    closeModalWindow(modalElement);
  });
}

//モーダルウインドウを閉じる
function closeModalWindow(modalElement){
  document.body.removeChild(modalElement);
}