import { TestBed } from '@angular/core/testing';

import { ResumePostService } from './resume-post.service';

describe('ResumePostService', () => {
  let service: ResumePostService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResumePostService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
