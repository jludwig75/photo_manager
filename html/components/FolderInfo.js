app.component('folder-info', {
    template:
    /*html*/
`
<span class ="component-title folder-info-item">{{ current_folder_name }}</span>
<span class ="folder-info-item" v-if="folderInfo != null">
    {{ dateString(folderInfo.create_time) }}
</span>
<span class ="folder-info-item" v-if="folderInfo != null">
    {{ folderInfo.image_count }} images
</span>
<span class ="folder-info-item" v-if="folderInfo != null">
    {{ sizeString(folderInfo.size_bytes) }}
</span>
<span class ="folder-info-item" style="float: right">
    <button :disabled="folderInfo == null || folderInfo.image_count > 0" v-on:click="deleteFolder" :key="folderInfo != null && folderInfo.image_count">Delete Folder</button>
</span>
<span class ="folder-info-item" style="float: right">
    <button v-on:click="refreshFolder">Refresh Folder</button>
</span>
`,
    props: {
        current_folder_name: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            folderInfo: null
        }
    },
    methods: {
        refreshFolder() {
            this.$emit('current-folder-refresh-requested');
        },
        deleteFolder() {
            if (confirm("Are you sure you want to delete folder '" + this.current_folder_name + "'?")) {
                axios.
                    delete('/folders/' + this.current_folder_name).
                    then(response => this.folderDeleted()).
                    catch(error => alert('Failure deleting folder "' + this.current_folder_name + '": ' + error));
            }
        },
        folderDeleted() {
            this.$emit('folder-deleted', this.current_folder_name);
        },
        updateFolderInfo(info) {
            this.folderInfo = info;
            this.folderInfo['create_time'] = new Date(1000 * info['create_time'])
        },
        getFolderInfo() {
            if (this.current_folder_name != null) {
                axios.
                    get('/folders/' + this.current_folder_name).
                    then(response => this.updateFolderInfo(response.data)).
                    catch(error => console.log('Failed to get image list: ' + error));
            }
        },
        dateString(date) {
            return date.toLocaleDateString('en-US');
        },
        getDisplayPrecision(number) {
            if (number < 10) {
                return 2;
            }
            if (number < 100) {
                return 1;
            }
            return 0;
        },
        sizeString(sizeBytes) {
            if (sizeBytes < 1024) {
                return sizeBytes + ' bytes';
            }
            sizeBytes /= 1024.0;
            if (sizeBytes < 1024) {
                return sizeBytes.toFixed(this.getDisplayPrecision(sizeBytes)) + '  KB';
            }
            sizeBytes /= 1024.0;
            return sizeBytes.toFixed(this.getDisplayPrecision(sizeBytes)) + ' MB';
        }
    },
    mounted() {
        this.getFolderInfo()
    }
})