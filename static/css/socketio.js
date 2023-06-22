socket = io('http://' + document.domain + location.port);

        socket.on('connect', function(onlineUsers) {
            var userList = document.getElementById('connect');
            userList.innerHTML = '';

            onlineUsers.forEach(function(user) {
                var listItem = document.createElement('li');
                listItem.textContent = user;
                userList.appendChild(listItem);
            });
        });