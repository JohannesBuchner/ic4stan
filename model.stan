data {
  int N;
  real t[N];
  real yobs[N];
}
parameters {
  real<lower=-3,upper=3> logA;
  real<lower=-3,upper=3> logT;
  real<lower=0,upper=1> phi;
  real<lower=-3,upper=3> lognoise;
}
transformed parameters {
  real A;
  real T;
  real noise;
  
  A <- pow(10, logA);
  T <- pow(10, logT);
  noise <- pow(10, lognoise);
}
model {
  real y[N];
  for (i in 1:N) {
    y[i] <- A * sin(2 * pi() * (t[i] / T + phi));
  }
  
  yobs ~ normal(y, noise);
}

