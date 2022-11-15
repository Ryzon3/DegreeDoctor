<script>
import { useStore } from "../stores/store";

export default {
    data() {
        const majors = [
            "Computer Science",
            "Information Technology Web Science",
            "Math",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Economics",
            "Psychology",
            "Sociology",
            "Philosophy",
            "English",
            "French",
            "German",
            "Spanish",
            "Italian",
            "Russian",
            "Chinese",
            "Japanese",
            "Arabic",
            "Other",
        ];
        const minors = [
            "Monkey Science",
            "Information Technology Web Science",
            "Math",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Economics",
            "Psychology",
            "Sociology",
            "Philosophy",
            "English",
            "French",
            "German",
            "Spanish",
            "Italian",
            "Russian",
            "Chinese",
            "Japanese",
            "Arabic",
            "Other",
        ];
        const pathways = [
            "None",
            "Art History, Theory, and Criticism",
            "Artificial Intelligence",
            "Behavioral and Cognitive Neuroscience",
            "Chinese Language",
            "Creative Design and Innovation",
            "Design, Innovation, and Society Pathway",
            "Economics",
            "Economics of Banking and Finance",
            "Economics of Decision-Making",
            "Economics of Healthcare Markets",
            "Economics of Policy and Regulations",
            "Economics of Quantitative Modeling",
            "Economics of Technology and Innovation",
            "Electronic Arts",
            "Environmental Futures",
            "Ethics, Integrity, and Social Responsibility",
            "Extent and Limits of Rationality",
            "Fact and Fiction",
            "Game Studies",
            "Gender, Race, Sexuality, Ethnicity, and Social Change",
            "Graphic Design",
            "History",
            "Information Technology and Web Sciences",
            "Interactive Media/Data Design",
            "Language",
            "Linguistics",
            "Literature and Creative Writing",
            "Living in a World of Data",
            "Logical Thinking",
            "Media and Culture",
            "Mind, Brain, and Intelligence",
            "Music and Culture",
            "Music Composition and Production",
            "Music Performance",
            "Philosophy",
            "Pre-Health Pathway",
            "Public Health",
            "Science, Technology, and Society",
            "Strategic Communication",
            "Studio Arts",
            "Sustainability",
            "Thinking with Science",
            "Transfer Student Arts and Humanities",
            "Transfer Student Social Science",
            "Understanding Human Behavior",
            "Video, Performance, and Social Practice",
            "Well-being: Body and Mind",
        ];
        const concentrations = [
            "None",
            "Crizbae is a Monkey1",
            "Crizbae is a Monkey2",
            "Crizbae is a Monkey3",
            "Crizbae is a Monkey4",
            "Crizbae is a Monkey5",
        ];
        return {
            store: useStore(),
            selectedMajors: [],
            degreeName: "",
            majorOptions: majors,
            filteredMajors: majors,
            selectedMinors: [],
            minorOptions: minors,
            filteredMinors: minors,
            selectedPathways: "None",
            pathwayOptions: pathways,
            filteredPathways: pathways,
            selectedConcentrations: "None",
            concentrationOptions: concentrations,
            filteredConcentrations: concentrations,
        };
    },
    methods: {
        addMajor(val) {
            if (val.length > 0) {
                if (!this.selectedMajors.includes(val)) {
                    this.selectedMajors.push(val);
                }
            }
        },
        addMinor(val) {
            if (val.length > 0) {
                if (!this.selectedMinors.includes(val)) {
                    this.selectedMinors.push(val);
                }
            }
        },
        filterMajor(val) {
            this.filteredMajors = this.majorOptions.filter((x) =>
                x.toLowerCase().includes(val.toLowerCase())
            );
        },
        filterMinor(val) {
            this.filteredMinors = this.minorOptions.filter((x) =>
                x.toLowerCase().includes(val.toLowerCase())
            );
        },
        filterPathway(val) {
            this.filteredPathways = this.pathwayOptions.filter((x) =>
                x.toLowerCase().includes(val.toLowerCase())
            );
        },
        addPathway(val) {
            if (val.length > 0) {
                if (!this.selectedPathways.includes(val)) {
                    this.selectedPathways.push(val);
                }
            }
        },
        filterConcentration(val) {
            this.filteredConcentrations = this.concentrationOptions.filter(
                (x) => x.toLowerCase().includes(val.toLowerCase())
            );
        },
        addConcentration(val) {
            if (val.length > 0) {
                if (!this.selectedConcentrations.includes(val)) {
                    this.selectedConcentrations.push(val);
                }
            }
        },
        submit() {
            let degree = {
                name: this.degreeName,
                majors: this.selectedMajors,
                minors: this.selectedMinors,
                pathway: this.selectedPathways,
                concentration: this.selectedConcentrations,
            };
            console.log(degree);
            this.$router.push("/degree");
        },
        processTranscript(data){
            var reader = new FileReader();
            reader.readAsText(data);
            reader.onload = function(){
                console.log(reader.result);
            }

        },
    },
};
</script>

<template>
    <div class="q-gutter-y-md column" style="max-width: 300px">
        <q-file color="teal" filled v-model="model" label="Label" @update:model-value="processTranscript">
        <template v-slot:prepend>
          <q-icon name="file_upload" />
        </template>
      </q-file>
    </div>

    <q-form
        class="full-width column wrap justify-center items-center content-center"
    >
        <p>Enter Your Plan Name:</p>
        <q-input
            v-model="degreeName"
            standout="bg-teal text-white"
            label="My Course Plan"
        />
        <p>Select Your Major(s):</p>
        <q-select
            v-model="selectedMajors"
            standout="bg-teal text-white"
            filled
            use-input
            use-chips
            multiple
            input-debounce="0"
            :options="filteredMajors"
            style="width: 250px"
            @new-value="addMajor"
            @input-value="filterMajor"
        />
        <p>Select Your Minor(s):</p>
        <q-select
            v-model="selectedMinors"
            standout="bg-teal text-white"
            filled
            use-input
            use-chips
            multiple
            input-debounce="0"
            :options="filteredMinors"
            style="width: 250px"
            @new-value="addMinor"
            @input-value="filterMinor"
        />
        <p>Select Your Pathway(s):</p>
        <q-select
            v-model="selectedPathways"
            standout="bg-teal text-white"
            filled
            use-input
            input-debounce="0"
            :options="filteredPathways"
            style="width: 250px"
            @new-value="addPathway"
            @input-value="filterPathway"
        />
        <p>Select Your Concentration(s):</p>
        <q-select
            v-model="selectedConcentrations"
            standout="bg-teal text-white"
            filled
            use-input
            input-debounce="0"
            :options="filteredConcentrations"
            style="width: 250px; padding-bottom: 20px"
            @new-value="addConcentration"
            @input-value="filterConcentration"
        />
        <div>
            <q-btn label="Submit" color="primary" @click="submit" />
        </div>
    </q-form>
</template>
