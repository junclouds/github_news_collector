// 获取按钮和状态元素
document.addEventListener('DOMContentLoaded', function() {
  const checkButton = document.getElementById('checkUpdates');
  const statusDiv = document.getElementById('status');
  
  // 添加按钮点击事件
  checkButton.addEventListener('click', function() {
    // 发送消息给Service Worker
    chrome.runtime.sendMessage({ action: 'checkUpdate' }, function(response) {
      // 显示状态信息
      statusDiv.style.display = 'block';
      setTimeout(function() {
        statusDiv.style.display = 'none';
      }, 2000);
    });
  });
}); 