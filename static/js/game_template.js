// Verbindung zum WebSocket-Server herstellen

    function hideElements() {
        var sBox = document.getElementById("Sbox");
        var helloLobby = document.getElementById("helloLobby");
        var listTitle = document.getElementById("listTitle");
        var lobbiesList = document.getElementById("lobbies-list")
        sBox.style.display = "none";
        helloLobby.style.display = "none";
        listTitle.style.display = "none";
        lobbiesList.style.display = "none";

    }

    var socket = io();

    // Ereignis 'user_update' empfangen und die Liste aktualisieren
    socket.on('user_update', function(users_list) {
        console.log('Aktualisierte Lobbies:', users_list);

        // Ungeordnete Liste leeren
        const lobbiesList = document.getElementById('lobbies-list');
        lobbiesList.innerHTML = '';

        // Spieler in die Liste einfügen
        users_list.forEach(function(player) {
          const listItem = document.createElement('li');
          listItem.textContent = player;
          lobbiesList.appendChild(listItem);
        });
    });

