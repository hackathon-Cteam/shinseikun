/**
 * リクエスト送信
 * @param {*} data リクエストデータ
 * @returns json形式のリクエスト結果
 */
export default async function requestPost(url, data) {
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