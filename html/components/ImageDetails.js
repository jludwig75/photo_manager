app.component('image-details', {
    template:
    /*html*/
`
<div class="image-detail-header">
    <span v-if="current_image != null">
        Properties of {{ current_image.name }}:
    </span>
</div>
<div class="image-detail" v-for="detail in getDetailsList(current_image)">
    <div class="image-detail-name">
        {{ detail.name }}
    </div>
    <div class="image-detail-value">
        <span v-if="current_image != null">
            {{ detail.value }}
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
        getDetailsList(image) {
            var detailsList = [];
            for (var key in image) {
                if (!image.hasOwnProperty(key)) {
                    continue;
                }
                newKey = key.toLocaleLowerCase();
                if (['name', 'index', 'link', 'thumbnail', 'format_mimetype'].includes(newKey)) {
                    continue;
                }
                value = image[key];
                if (value instanceof Date) {
                    value = value.toLocaleDateString('en-US') + ', ' + value.toLocaleTimeString('en-US')
                }
                if (newKey.includes('size') && Number.isFinite(value)) {
                    value = this.sizeString(value);
                }
                newKey = newKey.replace(/_bytes/g, '')
                detailsList.push({
                                    'name': this.formatKeyName(newKey),
                                    'value': value
                                })
            }
            return detailsList;
        },
        formatKeyName(name) {
            name = name.replace(/_/g, ' ')
            return name.charAt(0).toUpperCase() + name.slice(1);
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
    }
})