app.component('image-dialog', {
    template:
    /*html*/
`
<img v-if="current_image != null" class="dialog-img" :src="current_image.link">
<button v-on:click="deleteImage">Delete Image</button>
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