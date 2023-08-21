/**
 * Channel Info表示イベントの登録
 */
function registerChannelInfoEvent() {
  const closeClass = 'close-channel-info';
  const info = document.getElementById('channel-info');
  document.getElementById('button-channel-info').addEventListener('click', () => {
    info.classList.remove(closeClass);
  });

  document.querySelector('#close-channel-info svg').addEventListener('click', () => {
    info.classList.add(closeClass);
  });
}

/**
 * リクエスト送信
 * @param {*} data リクエストデータ
 * @returns json形式のリクエスト結果
 */
async function requestPost(url, data) {
  let responseData = null;
  await fetch(url,
  { method: 'POST', headers : { 'Content-type' : 'application/json; charset=utf-8' }, body : JSON.stringify(data) }).then((response) => {
    if (!response.ok) {
      return Promise.reject(new Error(`status code: ${response.status}`));
    }
    return response.json();
  }).then((data) => {
    responseData = data;
  });
  return responseData;
}

/**
 * メッセージを投稿
 * @param {String} messageText メッセージテキスト
 * @param {String} channelId メッセージテキスト
 */
function sendMessage(messageText, channelId) {
  message = messageText.trim();
  if (message.length) {
    try {
      requestPost('/post-message', { message, channelId });
    } catch (error) {
      console.log(error.message);
    }
  }
}

/**
 * チャット画面からのメッセージ投稿のイベント処理
 * @param {Element} input 入力欄要素
 * @param {String} channelId チャンネルID
 */
function sendMessageEvent(input, channelId) {
  sendMessage(input.value, channelId);
  input.value = '';
}

/**
 * メッセージ投稿イベントの登録
 */
function registerMessageSendEvent() {
  const messageInput = document.getElementById('input-message');
  const channelId = document.getElementById('channel-name').getAttribute('data-channel-id');
  // 送信ボタンクリック時
  messageInput.querySelector('svg path').addEventListener('click', () => {
    sendMessageEvent(messageInput.getElementsByTagName('textarea')[0], channelId);
  });

  // control + Enterもしくはcommand + Enterのキーの組み合わせが入力欄で押された時
  messageInput.querySelector('textarea').addEventListener('keydown', (event) => {
    if (((event.ctrlKey && !event.metaKey) || (!event.ctrlKey && event.metaKey)) && event.code === "Enter")  {
      sendMessageEvent(messageInput.getElementsByTagName('textarea')[0], channelId);
    }
  });
}

/**
 * メッセージ削除ボタン要素を生成
 * @returns 削除ボタンElement
 */
function createDeleteButton() {
  const deleteButton = document.createElement('button');
  deleteButton.setAttribute('type', 'button');
  deleteButton.setAttribute('class', 'delete-chat');
  deleteButton.innerText = '削除';
  return deleteButton;
}

/**
 * オーバーレイ要素を生成
 * @returns オーバーレイElement
 */
function createOverlay() {
  const overlay = document.createElement('div');
  overlay.setAttribute('id', 'overlay');
  overlay.classList.add('overlay');
  return overlay;
}

/**
 * メッセージ削除イベントの登録
 */
function registerDeleteMessageEvent() {
  const dateLineStyleClassName = 'date-line';
  document.querySelectorAll('.chat-message .chat').forEach((chat) => {
    chat.addEventListener('dblclick', (event) => {
      const message = event.target.closest('.chat-message');
      message.appendChild(createDeleteButton());
      message.querySelector('button').addEventListener('click', () => {
        // TODO: 削除ボタン押下後の処理
        console.log('メッセージ削除の処理呼び出し');

        // 不要な日時ラインを削除
        if (dateLineStyleClassName === message.previousElementSibling.className
            && dateLineStyleClassName === message.nextElementSibling.className) {
          message.previousElementSibling.remove();
        }
        message.remove();
        document.getElementById('overlay').remove();
      });

      // 削除ボタン以外をクリックした時
      document.getElementById('content').appendChild(createOverlay());
      document.getElementById('overlay').addEventListener('click', (event) => {
        message.querySelector('button').remove();
        event.target.remove();
      });
    });
  });
}

window.addEventListener('load', () => {
  // チャットエリアが下までスクロールされた状態で表示する
  document.getElementById('chat-area').scrollIntoView(false);
  // チャンネル情報表示の処理を登録
  registerChannelInfoEvent();
  // メッセージ投稿の処理を登録
  registerMessageSendEvent();

  // ログインが管理者であればメッセージ削除の処理を登録
  if (document.querySelector('#header #account a').dataset.usertype === 'admin') {
    registerDeleteMessageEvent();
  }
});