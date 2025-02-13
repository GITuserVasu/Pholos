import { Component, OnInit } from '@angular/core';
import { loadStripe } from '@stripe/stripe-js';
import { environment } from '../../../../src/environments/environment';

@Component({
    selector: 'app-price-list',
    templateUrl: './price-list.component.html',
    styleUrls: ['./price-list.component.css'],
    standalone: false
})
export class PriceListComponent implements OnInit {
  pricevalue:any = 19.99;
title = "angular-stripe";
  priceId = "price_1N8WgEF3xgXrekg2KjZJKCiy";
  product = {
    title: "Classic Peace Lily",
    subTitle: "Popular House Plant",
    description:
      "Classic Peace Lily is a spathiphyllum floor plant arranged in a bamboo planter with a blue & red ribbom and butterfly pick.",
    price: 99,
  };
  quantity = 1;
  stripePromise = loadStripe(environment.stripe_key);
ngOnInit(): void {
  
}

price(event:any){
  this.pricevalue =event.target.value
}

  async checkout(priceId:any, packageName:any) {

    
    // Call your backend to create the Checkout session.
    // When the customer clicks on the button, redirect them to Checkout.
    const stripe:any = await this.stripePromise;
    const { error } = await stripe.redirectToCheckout({
      mode: "subscription",
      lineItems: [{ price: priceId, quantity: this.quantity }],
      successUrl: `${window.location.href}/success/${packageName}`,
      cancelUrl: `${window.location.href}/failure`,
    });
    // If `redirectToCheckout` fails due to a browser or network
    // error, display the localized error message to your customer
    // using `error.message`.
    if (error) {
      console.log(error);
    }
  }

}
