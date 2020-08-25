// TODO better random url generator
function uniqueUrl(length) {
    let res = [];
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        res.push(chars.charAt(Math.floor(Math.random() * chars.length)));
    }
    return res.join('');
};

async function goToRoom() {
    const roomId = uniqueUrl(10);

    const response = await fetch('/create/' + roomId, {method: 'POST'});
    
    /* Conflict, room already exists, try again */
    if (response.status == 409) {
        await goToRoom();
        return;
    }

    if (!response.ok) {
        throw new Error('Network error');
    }

    window.location.pathname = roomId;
    console.log(window.location.href);
};