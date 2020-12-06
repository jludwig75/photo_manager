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
            <img class="image-list-item" :src="image.thumbNail" v-on:click="onClickImage(image)" v-on:dblclick="onDoubleClickImage(image)" height="90">
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
            imageList: [],
            selectedImage: null
        }
    },
    methods: {
        addImageDetails(image, details) {
        // image['file_date'] = new Date(1000 * details['create_time']);
        // image['size_bytes'] = details['size_bytes'];
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
        },
        updateImageData(imageData) {
            var index = imageData['userContext']
            this.addImageDetails(this.imageList[index], imageData)
            if (index == 0) {
                this.selectImage(this.imageList[index]);
            }
        },
        updateImageList(imageList) {
            var index = 0;
            for (const imageName of imageList) {
                image = {'index': index,
                        'name': imageName,
                        'link': '/folders/' + this.current_folder_name + '/images/' + imageName + '/content',
                        'thumbNail': '/folders/' + this.current_folder_name + '/images/' + imageName + '/thumbnail'};
                this.imageList.push(image);
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
            document.getElementById('image-' + image.index).scrollIntoView();
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
            }
        });
    }
})