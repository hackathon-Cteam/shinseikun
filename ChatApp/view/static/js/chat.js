import requestPost from './common/request.js';

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
 * メッセージを投稿
 * @param {String} messageText メッセージテキスト
 * @param {String} channelId メッセージテキスト
 */
async function sendMessage(messageText, channelId) {
  const message = messageText.trim();
  if (message.length) {
    try {
      await requestPost('/post-message', { message, channelId });
    } catch (error) {
      console.log(error.message);
    }
  }
}

/**
 * チャット画面からのメッセージ投稿のイベント処理
 * @param {String} messageText メッセージテキスト
 * @param {String} channelId チャンネルID
 */
async function sendMessageEvent(messageText, channelId) {
  try {
    await sendMessage(messageText, channelId);
    location.reload();
  } catch (error) {
    console.log(error.message);
    alert('メッセージを投稿できませんでした');
  }
}

/**
 * メッセージ投稿イベントの登録
 */
function registerMessageSendEvent() {
  const messageInput = document.getElementById('input-message');
  const channelId = document.getElementById('channel-name').getAttribute('data-channel-id');
  // 送信ボタンクリック時
  messageInput.querySelector('svg path').addEventListener('click', () => {
    sendMessageEvent(messageInput.getElementsByTagName('textarea')[0].value, channelId);
  });

  // control + Enterもしくはcommand + Enterのキーの組み合わせが入力欄で押された時
  messageInput.querySelector('textarea').addEventListener('keydown', (event) => {
    if (((event.ctrlKey && !event.metaKey) || (!event.ctrlKey && event.metaKey)) && event.code === "Enter")  {
      sendMessageEvent(messageInput.getElementsByTagName('textarea')[0].value, channelId);
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
 * メッセージ削除の処理
 * @param {Element} message チャットメッセージ要素
 * @param {Element} overlay 表示しているオーバーレイ要素
 */
async function deleteMessageEvent(message, overlay) {
  const messageId = message.getAttribute('data-message-id');
  try {
    await requestPost('/delete-message', { messageId });
    // 不要な日時ラインを削除
    const dateLineStyleClassName = 'date-line';
    if (!message.nextElementSibling && message.previousElementSibling.className === dateLineStyleClassName) {
        message.previousElementSibling.remove();
    }
    if (message.previousElementSibling.className === dateLineStyleClassName && message.nextElementSibling.className  === dateLineStyleClassName) {
        message.previousElementSibling.remove();
    }

    message.remove();
    overlay.remove();
  } catch (error) {
    console.log(error.message);
    alert('メッセージを削除できませんでした');
  }
}

/**
 * メッセージ削除イベントの登録
 */
function registerDeleteMessageEvent() {
  document.querySelectorAll('.chat-message .chat').forEach((chat) => {
    chat.addEventListener('dblclick', (event) => {
      const message = event.target.closest('.chat-message');
      message.appendChild(createDeleteButton());
      message.querySelector('button').addEventListener('click', () => {
        deleteMessageEvent(message, document.getElementById('overlay'));
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
  // チャンネル情報表示の処理を登録
  registerChannelInfoEvent();
  // メッセージ投稿の処理を登録
  registerMessageSendEvent();

  // ログインが管理者であればメッセージ削除の処理を登録
  if (document.querySelector('#header #account a').dataset.usertype === 'admin') {
    registerDeleteMessageEvent();
  }

  // チャットエリアが下までスクロールされた状態で表示する
  document.getElementById('chat-area').scrollIntoView(false);
});