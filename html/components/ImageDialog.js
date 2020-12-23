app.component('image-dialog', {
    template:
    /*html*/
`
<span v-if="current_image != null">
    <img v-if="current_image.media_type == 'image'" class="dialog-img" :src="current_image.path" :style="{ maxWidth: imageWidth + 'px', maxHeight: imageHeight + 'px' }">
    <video v-if="current_image.media_type == 'video'" width="853" height="480" controls>
        <source :src="current_image.path" :type="current_image.mime_type">
        Your browser does not support the video tag.
    </video>
    <button v-on:click="deleteImage">Delete Image</button>
</span>
`,
    props: {
        current_image: {
            type: Object,
            required: true
        },
        current_folder_name: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            imageWidth: 0,
            imageHeight: 0
        }
    },
    methods: {
        deleteImage() {
            if (confirm('Are you sure you want to delete image"' + this.current_image.name + '"?')) {
                axios.
                    delete('/folders/' + this.current_folder_name + '/images/' + this.current_image.name).
                    then(response => this.onDeleteSucceeded()).
                    catch(error => alert('Failure deleting image "' + this.current_image.name + '": ' + error));
            }
        },
        onDeleteSucceeded() {
            this.$emit('image-deleted', this.current_image);
            $( "#dialog" ).dialog("close");
        }
    },
    mounted() {
        const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        const dialogWidth = Math.floor((vw * 6) / 10);
        const dialogHeight = vh - 20;
        this.imageWidth = dialogWidth - 45;
        if (this.imageWidth < 640) {
            this.imageWidth = 640;  // Rather have a scrollbar at this size
        }
        this.imageHeight = dialogHeight - 90;
        if (this.imageHeight < 480) {
            this.imageHeight = 480;  // Rather have a scrollbar at this size
        }
    }
})