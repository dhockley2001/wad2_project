
$( document ).ready(function() {
    console.log( "ready!" );
      $("#filmLink").on('click',function (e) {
      $.ajax({
          type: 'POST',
          url: "{% url 'filmfanatics:get_film' %}",
          data: $(this).alt,
          success: function (json) {
                var title = json["title"]
                var director = json["director"]
                var cast = json["cast"]
                var picture = json["picture"]
                var synopsis = json["synopsis"]
                var release = json["release"]
                var review_number = json["review_number"]
                var average_rating = json["average_rating"]
                var modal = document.getElementById("filmModal")
                modal.find('.modal-title').text(title)
                $('#filmModal').modal('toggle')
          },
        error: function (response) {
          console.log(response)
        }
      })
      })

    $('#randButton').on('click',function (e) {
        $.ajax({
            type: 'GET',
            url: "{% url 'filmfanatics:get_random_film' %}",
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
                    var modal = document.getElementById("filmModal")
                    modal.find('.modal-title').text(title)
                    $('#filmModal').modal('show')
                },
            error: function (response) {
                console.log(response)
            }
        })
    })
});
