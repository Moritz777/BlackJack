socket = io('http://' + document.domain + location.port);

    socket.on('connect', function() {
      console.log('Socket connected');
      // Do something when connected, e.g., emit a custom event
      socket.emit('templateAccessed', { /* data if needed */ });
    });
