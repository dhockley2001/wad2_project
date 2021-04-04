// check document has loaded
$( document ).ready(function() {
    console.log( "ready!" );

    // when a film image has been clicked, display its information on a modal
      $( document ).on('click', '.filmLink', function (e) {
          // get url for function from element and the film name
            var url = $(this).attr("data-url");
            var name = $(this).attr("alt")
      $.ajax({
          type: 'POST',
          url: url,
          data: {film: name},
          success: function (json) {

              // parse json response
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
                var slug = json["slug"]

                // get the modal and update its information
                var modal = $("#filmModal")
                modal.find('.modal-title').text(title);
                modal.find('.views').text(views);
                modal.find('.director').text(director);
                modal.find('.cast').text(cast);
                modal.find('.synopsis').text(synopsis);
                modal.find('.picture').attr('src', picture);

                // change the url that the review button points to, passing the correct film as an arguement
                var review_button = $('#reviewButton');
                var review_url = review_button.attr("data-url");
                review_button.attr('href', review_url + slug + "/");

                // insert number of stars based on the rating
                var stars = modal.find('.avgRating');
                stars.empty();
                var i;
                for (i = 0; i < average_rating; i++){
                    var star = $('<span></span>').addClass("fa fa-star checked");
                    star.appendTo(stars);
                }


                // reset reviews panel from last modal
                $('.panel-body').empty();

                // insert review box for each review, with the correct information
                $.each(reviews, function(index, review) {
                    var firstDiv = $('<div></div>').addClass("media");
                    firstDiv.appendTo( ".panel-body");
                    var secondDiv = $('<div></div>').addClass("media-left");
                    secondDiv.appendTo(firstDiv);
                    console.log(review.profile_pic);
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

                // open the modal once all of the correct information has been inserted onto the modal
                $('#filmModal').modal('toggle');
          },
        error: function (response) {
          console.log(response)
        }
      })
      })

    // when the random button is clicked, find a random film and display its information on a modal
    $('#randButton').on('click',function (e) {
        // get url for function from element
            var url = $(this).attr("data-url");
        $.ajax({
            type: 'GET',
            url: url,
            success: function (json) {
                // parse json response
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
                    var slug = json['slug']

                    // get the modal and update its information
                    var modal = $("#filmModal");
                    modal.find('.modal-title').text(title);
                    modal.find('.views').text(views);
                    modal.find('.director').text(director);
                    modal.find('.cast').text(cast);
                    modal.find('.synopsis').text(synopsis);
                    modal.find('.picture').attr('src', picture);

                    // change the url that the review button points to, passing the correct film as an arguement
                    var review_button = $('#reviewButton');
                    var review_url = review_button.attr("data-url");
                    review_button.attr('href', review_url + slug + "/");

                    // insert number of stars based on the rating
                    var stars = modal.find('.avgRating');
                    stars.empty();
                    var i;
                    for (i = 0; i < average_rating; i++){
                        var star = $('<span></span>').addClass("fa fa-star checked");
                        star.appendTo(stars);
                    }

                    // reset review panel from previous modal opening
                    $('.panel-body').empty();

                    // insert review box for each review, with the correct information
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

    // when a modal is shown, update the save button based on whether the film already has been saved
    $( document ).on('shown.bs.modal', function (e) {
        // get the area where the button is placed
        var div = $(".saveFilm");

        // get both function urls
        var checkurl = div.attr("data-urlcheck");
        var saveurl = div.attr("data-urlsave");

        // get the film name
        var name = $("#filmModal").find('.modal-title').text();
        $.ajax({
            type : 'POST',
            url : checkurl,
            data : {name:name},
            success: function (json) {

                // reset the button
                div.empty();

                // parse json response, including whether the film is already saved or not
                var saved = json['saved']
                var slug = json['slug']

                // if it is saved, display remove button
                if (saved) {
                var button = $('<a id = "saveButton" class="btn btn-outline-info" role="button">Remove Film From Saved</a>');
                    button.attr('href', saveurl + slug + "/");
                    button.appendTo(div);
                // otherwise display save button
                } else {
                    var button = $('<a id = "saveButton" class="btn btn-outline-info" role="button">Save This Film</a>');
                    button.attr('href', saveurl + slug + "/");
                    button.appendTo(div);
                }

            },
            error: function(response){
                console.log(response);
            }
        })
    })


});
