app.component('image-details', {
    template:
    /*html*/
`
<div class="image-detail-header">
    <span v-if="current_image != null">
        Properties of {{ current_image.name }}:
    </span>
</div>
<div class="image-detail">
<div class="image-detail-name">
    Date Taken:
</div>
<div class="image-detail-value">
    <span v-if="current_image != null">
        12/23/2019 at 3:15 pm
    </span>
</div>
</div>
<div class="image-detail">
<div class="image-detail-name">
    File Date:
</div>
<div class="image-detail-value">
    <span v-if="current_image != null">
        {{ current_image.date.toLocaleDateString('en-US') + ', ' + current_image.date.toLocaleTimeString('en-US')}}
    </span>
</div>
</div>
<div class="image-detail">
<div class="image-detail-name">
    Size:
</div>
<div class="image-detail-value">
    <span v-if="current_image != null">
        {{ sizeString(current_image.size_bytes) }}
    </span>
</div>
</div>
`,
    props: {
        current_image: {
            required: true
        }
    },
    methods: {
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
    }
})