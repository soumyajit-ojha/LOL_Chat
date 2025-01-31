function declineFriendRequest(friend_request_id, uiUpdateFunction){
    var url = `/decline_friend_request/${friend_request_id}`
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: url,
        timeout: 5000,
        success: function(data) {
            if(data['response'] == "Friend request declined."){
                console.log(data.response)                
            }
            else if(data['response'] != null){
                console.log(data['response'])
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