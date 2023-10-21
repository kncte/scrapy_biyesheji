$(document).ready(function() {




    // 获取表格和停止按钮的引用
    var tableBody = $('#crawlTable tbody');
    var stopButton = $('#stopButton');

    // 向后端请求数据
    $.get('/get_crawl_tasks', function(data) {
        // 遍历返回的数据并将其添加到表格中
        data.forEach(function(task) {
            var row = $('<tr>');
            row.append($('<td>').text(task.id));  // 添加ID列
            row.append($('<td>').text(task.gjz));
            row.append($('<td>').text(task.task_id));
            row.append($('<td>').text(task.type));
            row.append($('<td>').text(task.start_time));
            row.append($('<td>').text(task.end_time));
            row.append($('<td>').text(task.Time));
            if (task.IsTrue === 1){
                row.append($('<td>').text("已完成"));
            }else {
                row.append($('<td>').text("未完成"));
                var stopButtonCell = $('<td>');
                var stopButton = $('<button>').text('Stop');
                stopButton.click(function() {
                    // 向后端发送停止请求，可以在这里使用 AJAX 请求
                        fetch('/stop_task', {
                            method: 'POST',
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('停止状态：',data.status);
                            alert('停止状态：'+ data.status)
                        })
                        .catch(error => {
                            console.error('请求失败:', error);
                        });

                });

                stopButtonCell.append(stopButton);
            }


            // 添加停止按钮并为其添加点击事件处理程序

            row.append(stopButtonCell);

            // 将行添加到表格中
            tableBody.append(row);
        });
    });
});

   function confirmDelete() {
    var result = confirm("确认删除吗？");

    if (result) {
        // 用户点击了确认按钮，发送请求
        var xhr = new XMLHttpRequest();
        xhr.open("DELETE", "/del_route", true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // 请求成功，可以执行一些操作
                console.log("删除成功");
                location.reload();
            }
        };
        xhr.send();
    } else {
        // 用户点击了取消按钮，可以不执行任何操作或执行相应的取消操作
        console.log("取消删除");
    }
}