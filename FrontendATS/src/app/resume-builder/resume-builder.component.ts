import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { ScriptService } from '../services/resumebuilder.service';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
//declare let pdfMake:any;
pdfMake.vfs = pdfFonts.pdfMake.vfs;

@Component({
  selector: 'app-resume-builder',
  templateUrl: './resume-builder.component.html',
  styleUrls: ['./resume-builder.component.css']
})
export class ResumeBuilderComponent implements OnInit {
  resumeBuilderForm: FormGroup;

  constructor(private formBuilder: FormBuilder, private scriptService: ScriptService) {
    
    this.resumeBuilderForm = JSON.parse(sessionStorage.getItem('form-data'))

    console.log('Loading External Scripts');
    this.scriptService.load('pdfMake', 'vfsFonts');
    

  }



  ngOnInit(): void {
    this.resumeBuilderForm = this.formBuilder.group({
      firstName: ['', [Validators.required]],
      lastName: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      phone: '',
      currentLocation: '',
      linkedIn: '',
      github: '',
      educationBlocks:this.formBuilder.array(
        [this.buildEducationBlock()]),
      experienceBlocks:this.formBuilder.array(
        [this.buildExperienceBlock()]),
      skillBlocks:this.formBuilder.array(
        [this.buildSkillBlock()]),
      projectBlocks:this.formBuilder.array(
        [this.buildProjectBlock()]),
      referenceBlocks:this.formBuilder.array(
        [this.buildReferenceBlock()])
    });
  }

  buildEducationBlock():FormGroup{
    return this.formBuilder.group({
      level: ['', [Validators.required]],
      school: ['', [Validators.required]],
      percentage: ['', [Validators.required]],
      passingYear: ['', [Validators.required]],

    });
  }

  buildExperienceBlock(): FormGroup {
  return this.formBuilder.group({
    title: ['', [Validators.required]],
    company: ['', [Validators.required]],
    location: ['', [Validators.required]],
    startDate: ['', [Validators.required]],
    endDate: ['', [Validators.required]]

    });
  }

  buildSkillBlock(): FormGroup {
  return this.formBuilder.group({
    skill: ['', [Validators.required]],
    years: ['', [Validators.required]]
    });
  }

  buildProjectBlock(): FormGroup {
    return this.formBuilder.group({
      name: ['', [Validators.required]],
      link: ['', [Validators.required]],
      projectDescription: ['', [Validators.required]]
    });
  }


  buildReferenceBlock(): FormGroup {
    return this.formBuilder.group({
        referee: ['', [Validators.required]],
        phone: ''
    });
  }

  save() {
    console.log(this.resumeBuilderForm);
    console.log('Saved: ' + JSON.stringify(this.resumeBuilderForm.value));
  }

  get educationBlocks(): FormArray {
    return this.resumeBuilderForm.get('educationBlocks') as FormArray;
  }
  addEducation() {
    this.educationBlocks.insert(0, this.buildEducationBlock());
  }
  get experienceBlocks(): FormArray {
    return this.resumeBuilderForm.get('experienceBlocks') as FormArray;
  }
  addExperience() {
    this.experienceBlocks.insert(0, this.buildExperienceBlock());
  }
  get skillBlocks(): FormArray {
    return this.resumeBuilderForm.get('skillBlocks') as FormArray;
  }
  addSkills() {
    this.skillBlocks.insert(0, this.buildSkillBlock());
  }
  get projectBlocks(): FormArray {
    return this.resumeBuilderForm.get('projectBlocks') as FormArray;
  }
  addProjects() {
    this.projectBlocks.insert(0, this.buildProjectBlock());
  }
  get referenceBlocks(): FormArray {
    return this.resumeBuilderForm.get('referenceBlocks') as FormArray;
  }
  addReference() {
    this.referenceBlocks.insert(0, this.buildReferenceBlock());
  }



  getDocumentDefinition() {
    sessionStorage.setItem('form-data', JSON.stringify(this.resumeBuilderForm.value));
     ​
    return {
      content:
      [
        {
          text: 'RESUME',
          bold: true,
          fontSize: 20,
          alignment: 'center',
          margin: [0, 0, 0, 20]
        },
        {
          columns:
          [
            [
              {
                text: this.formBuilder['resumeBuilderForm'].firstName,
                style: 'name'
              },
              {
                text: this.formBuilder['resumeBuilderForm'].lastName,
                style: 'name'
              },
              {
                text: this.formBuilder['resumeBuilderForm'].email,
                style: 'email'
              },
              {
                text: this.formBuilder['resumeBuilderForm'].phone,
              },
              {
                text: this.formBuilder['resumeBuilderForm'].currentLocation,
              },
              {
                text: this.formBuilder['resumeBuilderForm'].linkedIn,
                color: 'blue',
              },
              {
                text: this.formBuilder['resumeBuilderForm'].github,
                color: 'blue',
              },
            ],
          ]
        },

        {
          text: 'EDUCATION',
          style: 'header'
        },
        this.getEducationObject(this.formBuilder['resumeBuilderForm'].educationBlocks),

        {
          text: 'EXPERIENCE',
          style: 'header'
        },
        this.getExperienceObject(this.formBuilder['resumeBuilderForm'].experienceBlocks),

        {
          text: 'SKILLS',
          style: 'header'
        },
        this.getSkillObject(this.formBuilder['resumeBuilderForm'].skillBlocks),

        {
          text: 'PROJECTS',
          style: 'header'
        },
        this.getProjectObject(this.formBuilder['resumeBuilderForm'].projectBlocks),

        {
          text: 'REFERENCES',
          style: 'header'
        },
        this.getReferenceObject(this.formBuilder['resumeBuilderForm'].referenceBlocks),
      ],

      info: {
        title: this.formBuilder['resumeBuilderForm'].firstName + '_RESUME',
        author: this.formBuilder['resumeBuilderForm'].firstName,
        subject: 'RESUME',
        keywords: 'RESUME, ONLINE RESUME',
      },


      styles:
      {
        name:
        {
          fontSize: 16,
          bold: true
        }
      }
    };
  }

  getEducationObject(educationBlocks){
    return {
      table: {
        widths: ['*', '*', '*', '*'],
        body: [
          [{
            text: 'Level of Education',
            style: 'tableHeader'
          },
          {
            text: 'School',
            style: 'tableHeader'
          },
          {
            text: 'Passing Year',
            style: 'tableHeader'
          },
          {
            text: 'Result',
            style: 'tableHeader'
          },
          ],
          ...educationBlocks.map(ed => {
            return [ed.level, ed.school, ed.passingYear, ed.percentage];
          })
        ]
      }
    };

  }

  getExperienceObject(experienceBlocks){
    return {
      table: {
        widths: ['*', '*', '*', '*', '*'],
        body: [
          [{
            text: 'Job Title',
            style: 'tableHeader'
          },
          {
            text: 'Company',
            style: 'tableHeader'
          },
          {
            text: 'Location',
            style: 'tableHeader'
          },
          {
            text: 'Start Date',
            style: 'tableHeader'
          },
          {
            text: 'End Date',
            style: 'tableHeader'
          },
          ],
          ...experienceBlocks.map(ex => {
            return [ex.title, ex.company, ex.location, ex.startDate, ex.endDate];
          })
        ]
      }
    };

  }

  getSkillObject(skillBlocks){
    return {
      table: {
        widths: ['*', '*'],
        body: [
          [{
            text: 'SKILL',
            style: 'tableHeader'
          },
          {
            text: 'YEARS',
            style: 'tableHeader'
          },
          ],
          ...skillBlocks.map(sk => {
            return [sk.skill, sk.years];
          })
        ]
      }
    };

  }

  getProjectObject(projectBlocks){
    return {
      table: {
        widths: ['*', '*', '*'],
        body: [
          [{
            text: 'NAME OF PROJECT',
            style: 'tableHeader'
          },
          {
            text: 'LINK',
            style: 'tableHeader'
          },
          {
            text: 'PROJECT DESCRIPTION',
            style: 'tableHeader'
          },
          {
            text: 'Result',
            style: 'tableHeader'
          },
          ],
          ...projectBlocks.map(pr => {
            return [pr.name, pr.link, pr.projectDescription];
          })
        ]
      }
    };

  }

  getReferenceObject(referenceBlocks){
    return {
      table: {
        widths: ['*', '*'],
        body: [
          [{
            text: 'Referee',
            style: 'tableHeader'
          },
          {
            text: 'Phone',
            style: 'tableHeader'
          },

          ],
          ...referenceBlocks.map(re => {
            return [re.referee, re.phone];
          })
        ]
      }
    };

  }

  generatePdf(action = 'open') {
    console.log(pdfMake);
    const documentDefinition = this.getDocumentDefinition();

    switch (action) {
      case 'open': pdfMake.createPdf(documentDefinition).open(); break;
      case 'print': pdfMake.createPdf(documentDefinition).print(); break;
      case 'download': pdfMake.createPdf(documentDefinition).download(); break;

      default: pdfMake.createPdf(documentDefinition).open(); break;
    }

  }


}
