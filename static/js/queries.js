
$( document ).ready(function() {
    console.log( "ready!" );
      $( document ).on('click', '.filmLink', function (e) {
            var url = $(this).attr("data-url");
            var name = $(this).attr("alt")
      $.ajax({
          type: 'POST',
          url: url,
          data: {film: name},
          success: function (json) {
                var title = json["title"]
                var director = json["director"]
                var cast = json["cast"]
                var picture = json["picture"]
                var synopsis = json["synopsis"]
                var release = json["release"]
                var review_number = json["review_number"]
                var average_rating = json["average_rating"]
                var modal = $("#filmModal")
                modal.find('.modal-title').text(title);
                $('#filmModal').modal('toggle');
          },
        error: function (response) {
          console.log(response)
        }
      })
      })

    $('#randButton').on('click',function (e) {
            var url = $(this).attr("data-url");
        $.ajax({
            type: 'GET',
            url: url,
            success: function (json) {
                // open and change modal
                    var title = json["title"]
                    var director = json["director"]
                    var cast = json["cast"]
                    var picture = json["picture"]
                    var synopsis = json["synopsis"]
                    var release = json["release"]
                    var review_number = json["review_number"]
                    var average_rating = json["average_rating"]
                    var modal = $("#filmModal")
                    modal.find('.modal-title').text(title);
                    $('#filmModal').modal('toggle');
                },
            error: function (response) {
                console.log(response)
            }
        })
    })
});
