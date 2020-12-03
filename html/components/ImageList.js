app.component('image-list', {
    template:
    /*html*/
`
<div class="wrapper vertical-element">
    <ul class="image-list">
        <li class="image-list-item" v-for="image in imageList">
            <a :href="image.link">
                <img :src="image.thumbNail" height="100">
            </a>
            <br/>
            {{ image.date.toLocaleDateString('en-US') + ', ' + image.date.toLocaleTimeString('en-US')}}
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
            imageList: []
        }
    },
    methods: {
        updateImageData(imageData) {
            var index = imageData['userContext']
            this.imageList[index]['date'] = new Date(1000 * imageData['create_time']);
        },
        updateImageList(imageList) {
            var index = 0;
            for (const imageName of imageList) {
                this.imageList.push({'name': imageName,
                                    'link': '/folders/' + this.current_folder_name + '/images/' + imageName + '/content',
                                    'thumbNail': '/folders/' + this.current_folder_name + '/images/' + imageName + '/thumbnail'})
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
        }
    },
    mounted() {
        this.getImages()
    }
})