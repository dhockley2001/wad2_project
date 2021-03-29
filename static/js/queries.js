
$( document ).ready(function() {
    console.log( "ready!" );
      $("#filmLink").on('click',function (e) {
          const img = document.querySelector('#filmLink');
            var url = img.dataset.url
            var csrf = img.dataset.csrf
      $.ajax({
          type: 'POST',
          url: url,
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
            const button = document.querySelector('#randButton');
            var url = button.dataset.url
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
                    var elt = $('#filmModal .modal-title')
                    window.alert(elt)
                    $('#filmModal').modal('show');
                },
            error: function (response) {
                console.log(response)
            }
        })
    })
});
