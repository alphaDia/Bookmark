const siteUrl = '//127.0.0.1:8000';
const styleUrl = siteUrl + '/static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;


// Load CSS
const head = document.getElementsByTagName('head')[0];
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link);

// Load image container
const body = document.getElementsByTagName('body')[0];
boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>
`
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    const bookmarklet = document.getElementById('bookmarklet');
    const foundImages = document.querySelector('.images');
    
    foundImages.innerHTML = '';
    bookmarklet.style.display = 'block';

    bookmarklet.querySelector('#close')
    .addEventListener('click',
        function (e) {bookmarklet.style.display = 'none'}
    );

    // Select images
    const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image => {
        console.log(image)
        if (image.naturalWidth >= minWidth
            && image.naturalHeight >= minHeight) {
            // Create a new image to avoid all the extra unneeded attributes
            // from the original image
            const newImage = document.createElement('img');
            newImage.src = image.src;
            foundImages.append(newImage);
        }
    });

    // Bookmark image
    bookmarklet.addEventListener('click', function(e) {
        if (e.target.tagName.toLowerCase() === 'img') {
            console.log('Bookmark image clicked');
            window.open(siteUrl + '/images/create/?url='
                    + encodeURIComponent(e.target.src)
                    + '&title='
                    + encodeURIComponent(document.title),
                    '_blank')
        }
        this.style.display = 'none';
    })
}

bookmarkletLaunch()