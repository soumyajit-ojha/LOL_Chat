function sendFriendRequest(id, uiUpdateFunction) {
    const context = {
        "csrfmiddlewaretoken": csrfToken,
        "receiver_user_id": id,
    };

    $.ajax({
        type: "POST",
        url: "/friend_request/",
        timeout: 5000,
        data: context,
        success: function (data) {
            console.log(data.message);
            if (uiUpdateFunction) {
                uiUpdateFunction();
            }
            // Update the button dynamically
            const sendFriendRequestBtn = document.getElementById("id_send_friend_request_btn");
            if (sendFriendRequestBtn) {
                sendFriendRequestBtn.classList.remove("btn-primary");
                sendFriendRequestBtn.classList.add("btn-danger");
                sendFriendRequestBtn.textContent = "Cancel Friend Request";

                // Update button action to cancel the friend request
                sendFriendRequestBtn.onclick = function () {
                    cancelFriendRequest(id, onFriendRequestCancelled);
                };
            }
        },
        error: function (xhr) {
            console.error("Error sending friend request:", xhr.responseJSON?.message || "Unknown error");
            alert(xhr.responseJSON?.message || "Failed to send friend request.");
        },
    });
}

function cancelFriendRequest(id, uiUpdateFunction) {
    const context = {
        "csrfmiddlewaretoken": csrfToken,
        "receiver_user_id": id,
    };

    $.ajax({
        type: "POST",
        url: "/friend_request/cancel/", // Adjust URL for cancel endpoint
        timeout: 5000,
        data: context,
        success: function (data) {
            console.log(data.message);
            // Revert the button back to "Send Friend Request"
            if(uiUpdateFunction){
                uiUpdateFunction();
            }
            const sendFriendRequestBtn = document.getElementById("id_send_friend_request_btn");
            if (sendFriendRequestBtn) {
                sendFriendRequestBtn.classList.remove("btn-danger");
                sendFriendRequestBtn.classList.add("btn-primary");
                sendFriendRequestBtn.textContent = "Send Friend Request";

                // Update button action to send the friend request again
                sendFriendRequestBtn.onclick = function () {
                    sendFriendRequest(id, onFriendRequestSent);
                };
            }
        },
        error: function (xhr) {
            console.error("Error canceling friend request:", xhr.responseJSON?.message || "Unknown error");
            alert(xhr.responseJSON?.message || "Failed to cancel friend request.");
        },
    });
}
