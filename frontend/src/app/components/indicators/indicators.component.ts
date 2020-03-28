import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { DataService } from '../../services/data.service';


@Component({
  selector: 'app-indicators',
  templateUrl: './indicators.component.html',
  styleUrls: ['./indicators.component.css'],
})
export class IndicatorsComponent implements OnInit {
  constructor(private dataService:DataService) { }

  @Input() equity:string;
  @Input() model:string;

  data:any[];

  ngOnInit() {
    console.log('model is', this.model);
  }

  ngOnChanges() {
    // create header using child_id
    console.log('model is', this.model);
    console.log('equity is', this.equity);
    let modelNumber = this.model.charAt(this.model.length-1);
    this.dataService.getModelInformation(modelNumber, this.equity).subscribe(result => {
      this.data = result['data'];
      console.log('data coming into indicators is', this.data);
    })
  }
  

}
