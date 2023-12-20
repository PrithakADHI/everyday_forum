
    function followUser(userId) {
      // Perform the follow action using AJAX
      $.get("{% url 'add_follower_ajax' follower_id=0 %}".replace("0", userId), function(data) {
        // Handle the response
        console.log(data);

        // Update the page content
        if (data.status === 'success') {
          // Update follower and following counts
          $('#followerCount').text(data.followerCount);
          $('#followingCount').text(data.followingCount);

          // Update "Follow" link to "Unfollow"
          $('#followLink').text('Unfollow');
          $('#followLink').attr('onclick', 'return unfollowUser(' + userId + ')');

          // Manipulate the browser history
          var stateObj = { userId: userId, action: 'follow' };
          window.history.replaceState(stateObj, "Followed user", window.location.href);
        }
      });
      return false;  // Prevent default anchor tag behavior
    }

    function unfollowUser(userId) {
      // Perform the unfollow action using AJAX
      $.get("{% url 'delete_follower_ajax' follower_id=0 %}".replace("0", userId), function(data) {
        // Handle the response
        console.log(data);

        // Update the page content
        if (data.status === 'success') {
          // Update follower and following counts
          $('#followerCount').text(data.followerCount);
          $('#followingCount').text(data.followingCount);

          // Update "Unfollow" link to "Follow"
          $('#followLink').text('Follow');
          $('#followLink').attr('onclick', 'return followUser(' + userId + ')');

          // Manipulate the browser history
          var stateObj = { userId: userId, action: 'unfollow' };
          window.history.replaceState(stateObj, "Unfollowed user", window.location.href);
        }
      });
      return false;  // Prevent default anchor tag behavior
    }
