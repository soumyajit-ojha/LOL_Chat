function acceptFriendRequest(friend_request_id, uiUpdateFunction){
    var url = `/accept_friend_request/${friend_request_id}`
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: url,
        timeout: 5000,
        success: function(data) {
            if(data['message'] == "Friend request accepted."){
                // ui is updated
            }
            else if(data['message'] != null){
                console.log(data['message'])
            }
        },
        error: function(data) {
            console.error("ERROR...", data)
            alert("Something went wrong.",friend_request_id)
        },
        complete: function(data){
            uiUpdateFunction()
        }
    });
}