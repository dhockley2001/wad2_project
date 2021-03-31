
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
                var views = json["views"]
                var review_number = json["review_number"]
                var average_rating = json["average_rating"]
                var reviews = json["reviews"]

                var modal = $("#filmModal")
                modal.find('.modal-title').text(title);
                modal.find('.views').text(views);
                modal.find('.director').text(director);
                modal.find('.cast').text(cast);
                modal.find('.synopsis').text(synopsis);

                $('.panel-body').empty();

                $.each(reviews, function(index, review) {
                    var firstDiv = $('<div></div>').addClass("media");
                    firstDiv.appendTo( ".panel-body");
                    var secondDiv = $('<div></div>').addClass("media-left");
                    secondDiv.appendTo(firstDiv);
                    var img = $('<img>').addClass("media-object").css("width","60px").attr('src', review.profile_pic);
                    img.appendTo(secondDiv);
                    var thirdDiv = $('<div></div>').addClass("media-body");
                    thirdDiv.appendTo(firstDiv);
                    var heading = $('<h4></h4>').addClass("media-heading").text(review.username);
                    heading.appendTo(thirdDiv);
                    var paragraph = $('<p></p>').text(review.comment);
                    paragraph.appendTo(thirdDiv);
                    var fourthDiv = $('<div></div>').addClass("media-right");
                    fourthDiv.appendTo(firstDiv);
                    var i;
                    for (i = 0; i < review.rating; i++){
                        var star = $('<span></span>').addClass("fa fa-star checked");
                        star.appendTo(fourthDiv);
                    }
                    firstDiv.append('<br>')

                });
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
                    var views = json["views"]
                    var release = json["release"]
                    var review_number = json["review_number"]
                    var average_rating = json["average_rating"]
                    var reviews = json["reviews"]

                    var modal = $("#filmModal")
                    modal.find('.modal-title').text(title);
                    modal.find('.views').text(views);
                    modal.find('.director').text(director);
                    modal.find('.cast').text(cast);
                    modal.find('.synopsis').text(synopsis);

                    $('.panel-body').empty();

                    $.each(reviews, function(index, review) {
                        var firstDiv = $('<div></div>').addClass("media");
                        firstDiv.appendTo( ".panel-body");
                        var secondDiv = $('<div></div>').addClass("media-left");
                        secondDiv.appendTo(firstDiv);
                        var img = $('<img>').addClass("media-object").css("width","60px").attr('src', review.profile_pic);
                        img.appendTo(secondDiv);
                        var thirdDiv = $('<div></div>').addClass("media-body");
                        thirdDiv.appendTo(firstDiv);
                        var heading = $('<h4></h4>').addClass("media-heading").text(review.username);
                        heading.appendTo(thirdDiv);
                        var paragraph = $('<p></p>').text(review.comment);
                        paragraph.appendTo(thirdDiv);

                        var fourthDiv = $('<div></div>').addClass("media-right");
                        fourthDiv.appendTo(firstDiv);

                        var i;
                        for (i = 0; i < review.rating; i++){
                            var star = $('<span></span>').addClass("fa fa-star checked");
                            star.appendTo(fourthDiv);
                        }
                        firstDiv.append('<br>')
                    });
                    $('#filmModal').modal('toggle');
                },
            error: function (response) {
                console.log(response)
            }
        })
    })
});
