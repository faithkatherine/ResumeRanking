import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobPostComponent } from './add-job-post.component';

describe('AddJobPostComponent', () => {
  let component: AddJobPostComponent;
  let fixture: ComponentFixture<AddJobPostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddJobPostComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddJobPostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
