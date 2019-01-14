$(document).foundation();

$(document).ready(new function () {
    const apikey = "07ac4b0205ef1ba23347f5901bdf968c";
    const userid = "johncarl81";
    const flickrUrl = "https://api.flickr.com/services/rest/?" +
        "method=flickr.photos.search" +
        "&api_key=" + apikey +
        "&user_id=" + userid +
        "&format=json" +
        "&nojsoncallback=1" +
        "&per_page=24";
    $.getJSON({
        url: flickrUrl,
        success: function(response) {
            const gallery = document.createDocumentFragment();
            response.photos.photo.forEach(function(image) {
                const thumbnailUrl = "https://farm" + image.farm + ".staticflickr.com/" +
                    image.server + "/" +
                    image.id + "_" + image.secret + ".jpg";

                const imageUrl = "https://www.flickr.com/photos/" + userid + "/" + image.id;

                // <div class="cell small-6 medium-4 large-2">
                //   <a href="imageUrl">
                //     <img class="thumbnail" src="thumbnailUrl">
                //   </a>
                // </div>

                const imageDiv = document.createElement("div");
                imageDiv.classList.add("cell");
                imageDiv.classList.add("small-6");
                imageDiv.classList.add("medium-4");
                imageDiv.classList.add("large-2");

                const imageLink = document.createElement("a");
                imageLink.href = imageUrl;
                imageDiv.appendChild(imageLink);

                const imageImg = document.createElement("img");
                imageImg.className = "thumbnail";
                imageImg.setAttribute("src", thumbnailUrl);
                imageLink.appendChild(imageImg);

                gallery.appendChild(imageDiv);
            });

            document.getElementById("gallery").appendChild(gallery);
        },
        error: function(e) {
            console.error("Error fetching images ", e);
        }});
});
