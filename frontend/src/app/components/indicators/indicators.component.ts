import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { DataService } from '../../services/data.service';


@Component({
  selector: 'app-indicators',
  templateUrl: './indicators.component.html',
  styleUrls: ['./indicators.component.css'],
})
export class IndicatorsComponent implements OnInit {
  constructor(private dataService:DataService) { }

  @Input() modelID:string;

  data:any[];

  ngOnInit() {
    console.log('model ID is', this.modelID);
  }

  ngOnChanges() {
    // create header using child_id
    console.log('model is', this.modelID);

    this.dataService.getModelInformation(this.modelID).subscribe(result => {
      this.data = result['data'];
      console.log('data coming into indicators is', this.data);
    })
  }
  

}
