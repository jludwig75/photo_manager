app.component('image-dialog', {
    template:
    /*html*/
`
<span v-if="current_image != null">
    <img v-if="current_image.media_type == 'image'" class="dialog-img" :src="current_image.path">
    <video v-if="current_image.media_type == 'video'" width="640" height="480" controls>
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
    }
})