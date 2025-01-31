function sendFriendRequest(id, uiUpdateFunction) {
    const context = {
        "csrfmiddlewaretoken": csrfToken,
        "receiver_user_id": id,
    };

    $.ajax({
        type: "POST",
        url: "/send_friend_request/",
        timeout: 5000,
        data: context,
        success: function (data) {
            console.log(data.message);
            if (uiUpdateFunction) {
                uiUpdateFunction();
            }
            // Update the button dynamically
            const cancelRequestBtn = document.getElementById("id_cancel_friend_request_btn");
            if (cancelRequestBtn) {
                cancelRequestBtn.classList.remove("btn-primary");
                cancelRequestBtn.classList.add("btn-danger");
                cancelRequestBtn.textContent = "Cancel Friend Request";

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
        url: "/cancel_friend_request/", // Adjust URL for cancel endpoint
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
