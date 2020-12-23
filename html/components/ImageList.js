app.component('image-list', {
    template:
    /*html*/
`
<div class="wrapper vertical-element">
    <ul class="image-list">
        <li
          class="image-list-item"
          v-for="image in imageList"
          :key="image.index"
          :class="{ selected: selectedImage != null && selectedImage.index == image.index }"
          :id="'image-' + image.index"
        >
            <!-- <img class="image-list-item" :src="image.thumbnailPath" v-on:click="onClickImage(image)" v-on:dblclick="onDoubleClickImage(image)"> -->
            <!-- This div below replaces the image with a background so the user doesn't try to download the 
                 thumbnail image thinking they will get the full size image. I left the old code in, because
                 there might be a performance issue using the background image technique.
             -->
            <div class="img-replacement" v-on:click="onClickImage(image)" v-on:dblclick="onDoubleClickImage(image)" :style="{ backgroundImage: 'url(' + image.thumbnailPath + ')' }"></div>
        </li>
    </ul>
    <br/>
</div>
`,
    props: {
        current_folder_name: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            fetchList: [],
            imageList: [],
            selectedImage: null
        }
    },
    methods: {
        addImageDetails(image, details) {
            for (var key in details) {
                if (['name', 'userContext'].includes(key)) {
                    continue;
                }
                if (key in image) {
                    continue
                }
                value = details[key]
                if (key.includes('date') && Number.isFinite(value)) {
                    try {
                        value = new Date(1000 * value);
                    } catch {
                        /* Must not be a time stamp */
                    }
                }
                image[key] = value
            }
            this.imageList.push(image);
        },
        updateImageData(imageData) {
            var index = imageData['userContext']
            this.addImageDetails(this.fetchList[index], imageData)
            if (index == 0) {
                this.selectImage(this.imageList[index]);
            }
        },
        updateImageList(imageList) {
            this.fetchList = [];
            var index = 0;
            for (const imageName of imageList) {
                image = {'index': index,
                        'name': imageName};
                this.fetchList.push(image);
                axios.
                    get('/folders/' + this.current_folder_name + '/images/' + imageName + '?userContext=' + index).
                    then(response => this.updateImageData(response.data)).
                    catch(error => console.log('Failed to get image stats for image' + imageName + ': ' + error));
                index += 1;
            }
        },
        getImages() {
            if (this.current_folder_name != null) {
                axios.
                    get('/folders/' + this.current_folder_name + '/images').
                    then(response => this.updateImageList(response.data)).
                    catch(error => console.log('Failed to get image list: ' + error));
            }
        },
        selectImage(image) {
            this.selectedImage = image;
            var imageId = 'image-' + image.index;
            if (!this.isElementInViewport(imageId)) {
                document.getElementById(imageId).scrollIntoView(false);
            }
            this.$emit('image-selected', image);
        },
        onClickImage(image) {
            this.selectImage(image);
        },
        onDoubleClickImage(image) {
            this.selectImage(image);
            showDialog();
        },
        advanceImage(forward = true) {
            if (forward) {
                if (this.selectedImage.index < this.imageList.length - 1) {
                    this.selectImage(this.imageList[this.selectedImage.index + 1]);
                }
            } else {
                if (this.selectedImage.index > 0) {
                    this.selectImage(this.imageList[this.selectedImage.index - 1]);
                }
            }
        },
        imagesPerRow() {
            if (this.imageList.length < 2) {
                return this.imageList.length;
            }
            var firstElementId = 'image-' + this.imageList[0].index;
            var firstElementOffset = document.getElementById(firstElementId).offsetTop;
            itemsPerRow = 0;
            for (image of this.imageList) {
                var divId = 'image-' + image.index;
                if (document.getElementById(divId).offsetTop != firstElementOffset) {
                    break;
                }
                itemsPerRow++;
            }

            return itemsPerRow;
        },
        isElementInViewport (elId) {
            var el = document.getElementById(elId);

            // Special bonus for those using jQuery
            if (typeof jQuery === "function" && el instanceof jQuery) {
                el = el[0];
            }

            var rect = el.getBoundingClientRect();

            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
                rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
            );
        }
    },
    mounted() {
        this.getImages();
        window.addEventListener('keydown', (e) => {
            if (e.key == 'ArrowLeft') {
                this.advanceImage(false);
            } else if (e.key == 'ArrowRight') {
                this.advanceImage();
            } else if (e.key == 'Enter') {
                var t = this.selectedImage;
                this.selectedImage = null;
                this.selectedImage = t;
                showDialog();
                // Do this to prevent enter key from closing dialog.
                // Not only is behavior not intuitive for this app,
                // but pressing enter on an image shows the dialog,
                // but the user never sees it because the dialog closes
                // right away because of this enter key event.
                e.preventDefault();
            } else if (e.key == 'ArrowDown') {  // TODO: Disable when dialog is open
                if (this.selectedImage == null || this.imageList.length == 0) {
                    return;
                }
                if (this.selectedImage.index < this.imageList.length - 1) {
                    var imagesPerRow = this.imagesPerRow();
                    var fullRows = Math.floor(this.imageList.length / imagesPerRow);
                    var firstIndexOnLastRow = fullRows * imagesPerRow;
                    if (firstIndexOnLastRow == this.imageList.length) {
                        firstIndexOnLastRow -= imagesPerRow;
                    }
                    if (this.selectedImage.index >= firstIndexOnLastRow) {
                        return;
                    }
                    var newIndex = this.selectedImage.index + imagesPerRow;
                    if (newIndex > this.imageList.length - 1) {
                        newIndex = this.imageList.length - 1;
                    }
                    this.selectImage(this.imageList[newIndex]);
                }
            } else if (e.key == 'ArrowUp') {  // TODO: Disable when dialog is open
                if (this.selectedImage == null || this.imageList.length == 0) {
                    return;
                }
                var imagesPerRow = this.imagesPerRow();
                if (this.selectedImage.index > 0) {
                    if (this.selectedImage.index < imagesPerRow) {
                        return;
                    } else {
                        var newIndex = this.selectedImage.index - imagesPerRow;
                        this.selectImage(this.imageList[newIndex]);
                    }
                }
            }
        });
    }
})