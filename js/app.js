const FLICKR_CONFIG = Object.freeze({
    // Public, read-only Flickr key; it only allows searching public photos.
    API_KEY: "07ac4b0205ef1ba23347f5901bdf968c",
    USER_ID: "johncarl81",
    PHOTO_COUNT: 24
});

function buildSearchUrl() {
    const params = new URLSearchParams({
        method: "flickr.photos.search",
        api_key: FLICKR_CONFIG.API_KEY,
        user_id: FLICKR_CONFIG.USER_ID,
        format: "json",
        nojsoncallback: "1",
        per_page: String(FLICKR_CONFIG.PHOTO_COUNT)
    });
    return "https://api.flickr.com/services/rest/?" + params;
}

function buildPhotoCell(photo) {
    // <div class="cell small-6 medium-4 large-2"><a href="..."><img class="thumbnail" src="..."></a></div>
    const cell = document.createElement("div");
    cell.classList.add("cell", "small-6", "medium-4", "large-2");

    const link = document.createElement("a");
    link.href = "https://www.flickr.com/photos/" + FLICKR_CONFIG.USER_ID + "/" + photo.id;
    cell.appendChild(link);

    const image = document.createElement("img");
    image.className = "thumbnail";
    image.loading = "lazy";
    image.alt = photo.title;
    image.src = "https://live.staticflickr.com/" + photo.server + "/" + photo.id + "_" + photo.secret + "_n.jpg";
    link.appendChild(image);

    return cell;
}

async function loadGallery() {
    try {
        const response = await fetch(buildSearchUrl());
        const result = await response.json();
        const gallery = document.createDocumentFragment();
        result.photos.photo.forEach(photo => gallery.appendChild(buildPhotoCell(photo)));
        document.getElementById("gallery").appendChild(gallery);
    } catch (error) {
        console.error("Error fetching images ", error);
    }
}

document.addEventListener("DOMContentLoaded", loadGallery);
