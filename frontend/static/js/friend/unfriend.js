function removeFriend(id, uiUpdateFunction) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // Get CSRF token
    const context = {
        csrfmiddlewaretoken: csrfToken,
        removee_id: id,
    };

    $.ajax({
        type: "POST",
        url: "/unfriend/",
        timeout: 5000,
        data: context,
        success: function (data) {
            console.log(data.response);
            if (uiUpdateFunction) {
                uiUpdateFunction();
            }

            // Update the button dynamically
            const unfriendBtn = document.getElementById("id_unfriend_btn");
            if (unfriendBtn) {
                unfriendBtn.classList.add("btn-primary");
                unfriendBtn.textContent = "Send Friend Request";

                // Update button action to send the friend request again
                unfriendBtn.onclick = function () {
                    sendFriendRequest(id, onFriendRequestSent);
                };
            }
        },
        error: function (data) {
            console.error("Error while unfriending:", data.responseJSON?.response || "Unknown error");
            alert(data.responseJSON?.response || "Failed to unfriend.");
        },
    });
}
