import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddResumesComponent } from './add-resumes.component';

describe('AddResumesComponent', () => {
  let component: AddResumesComponent;
  let fixture: ComponentFixture<AddResumesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddResumesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddResumesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
