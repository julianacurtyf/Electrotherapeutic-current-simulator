import numpy as np
from django.db import models
from scipy import signal


class Current(models.Model):
    intensity = models.FloatField()
    carrier = models.FloatField()

    class Meta:
        abstract = True

    def sinusoidal(self, carrier):
        """"Create an array that corresponds to a sinusoidal wave

         Parameters
         ----------
         carrier : float
             the frequency, in Hertz, of the sinusoidal wave

         Returns
         -------
         array
             a array that corresponds to the value of the current on time
        """
        t = self.get_t()
        sinusoidalWave = self.intensity * np.sin(2 * np.pi * carrier * t)

        return sinusoidalWave

    def square(self, carrier):
        """Create an array that corresponds to a square wave, duty cicle is 50%

        Parameters
        ----------
        carrier : float
            the frequency, in Hertz, of the square wave

        Returns
        -------
        array
            a array that corresponds to the value of the current on time
       """
        t = self.get_t()
        squareWave = self.intensity * signal.square(2 * np.pi * carrier * t, duty=0.5)

        return squareWave

    def triangular(self, carrier):
        """Create an array that corresponds to a triangular wave

        Parameters
        ----------
        carrier : float
            the frequency, in Hertz, of the triangular wave

        Returns
        -------
        array
            a array that corresponds to the value of the current on time
       """
        t = self.get_t()
        triangularWave = self.intensity * signal.sawtooth(2 * np.pi * carrier * t, 0.5)

        return triangularWave

    def ramp(self, rise, on, decay, off):
        """Create an array that corresponds to a ramp

        Parameters
        ----------
        rise : float
            the time, in seconds, that takes to the current gets to it's higher value
        on : float
            the time, in seconds, that the current is constant in it's higher value (muscle contraction)
        decay : float
            the time, in seconds, that takes to the current gets to zero, from it's higher value
        off : float
            the time, in seconds, that the current is constant in zero (muscle relaxation)

        Returns
        -------
        array
            a array that corresponds to the value of the ramp during the treatment
       """
        timer = 2
        t = self.get_t()
        time = np.arange(0, rise, 1e-5)
        riseRamp = 0.5 * signal.sawtooth(2 * np.pi * time / rise) + 0.5

        time = np.arange(0, decay, 1e-5)
        decayRamp = 0.5 * signal.sawtooth(2 * np.pi * time / decay, 0) + 0.5

        constant = on
        time_const = np.arange(0, constant, 1e-5)
        time_off = np.arange(0, off, 1e-5)

        ramp = list(riseRamp) + list(np.ones(len(time_const))) + list(decayRamp) + list(np.zeros(len(time_off)))

        resized_ramp = np.array(ramp * (int(timer * 60 / (on + off + rise + decay) + 1)))

        resized_ramp = resized_ramp[:len(t)]

        return resized_ramp

    def burst(self, frequency, duty):
        """Create an array that has value 1 when burst mode is 'on' and 0 when is 'off'

        Parameters
        ----------
        frequency : float
            the frequency, in Hertz, of the burst
        duty : float
            the percentage of the period that the current is on

        Returns
        -------
        array
            a array that corresponds to the value of the ramp during the treatment
        """
        t = self.get_t()
        burst = (0.5 * signal.square(2 * np.pi * frequency * t, duty=duty) + 0.5)

        return burst

    def get_t(self,p=10e-6):
        timer = 10 * 1/self.carrier
        t = np.arange(0, timer, p)
        return t

class Russa(Current):
    burst_hz = models.FloatField()
    rise = models.FloatField()
    on = models.FloatField()
    decay = models.FloatField()
    off = models.FloatField()
    duty = models.FloatField()

    def wave(self):
        """Create an array that corresponds to a Russian Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        carrier = 2.5e3 
        self.duty = self.duty/100
        return self.sinusoidal(carrier) * self.burst(self.burst_hz, self.duty) * self.ramp(self.rise, self.on,
                                                                                                self.decay, self.off)

    def __str__(self):
        return "A Corrente Russa é uma corrente alternada de média frequência (2,5 kHz) modulada em \
            bursts retangulares usada para produzir fortalecimento muscular sem desconforto significante \
                para o paciente."


class Aussie(Current):
    burst_hz = models.FloatField()
    burst_ms = models.FloatField()
    rise = models.FloatField()
    on = models.FloatField()
    decay = models.FloatField()
    off = models.FloatField()

    def wave(self):
        """Create an array that corresponds to a Aussie Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        duty = self.burst_ms * self.burst_hz * 1e-3
        return self.sinusoidal(self.carrier) * self.burst(self.burst_hz, duty) * self.ramp(self.rise, self.on,
                                                                                                self.decay, self.off)

    def __str__(self):
        return "A corrente Aussie (Corrente Australiana) é uma corrente alternada de média frequência \
            liberada em bursts curtos (1 kHz/ duração do burst de 2 ms ou 4 kHz/ duração do burst de 4 ms) \
                usada para produzir torque muscular máximo ou analgesia respectivamente, sem desconforto \
                    significante para o paciente."


class TENS(Current):

    mode = models.CharField(max_length=3,choices=[('C','Continuous'), ('B','Burst modulation'), ('VIF','Automatic variation of intensity and frequency')])
    fase = models.FloatField()

    def wave(self):
        """Create an array that corresponds to a TENS Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """

        if self.mode == "C":
            self.carrier_tens = self.carrier  # Frequência: ajustável de 1 - 250 Hz ±10%
            self.duty = self.fase * self.carrier_tens * 2
            return self.square(1 / (2 * self.fase)) * self.burst(self.carrier_tens, self.duty)

        elif self.mode == "B":
            self.carrier_tens = 250  # Frequência fixa em 250 Hz ±10%
            self.burst_freq = 2  # Frequência do Burst de 2 Hz ±10%
            self.burst_duty = 2 * self.fase * self.burst_freq
            self.duty = 2 * self.fase * self.carrier_tens
            return self.square(1 / (2 * self.fase)) * self.burst(self.carrier_tens, self.duty) * self.burst(self.burst_freq,
                                                                                                       self.burst_duty)

        elif self.mode == "VIF":
            self.carrier_tens = self.carrier  # Frequência: 2 - 247 Hz ±10%
            self.duty = 2 * self.fase * self.carrier_tens
            return self.square(1 / (2 * self.fase)) * self.burst(self.carrier_tens, self.duty)

    def __str__(self):
        return "A forma de onda quadrática simétrica bifásica da corrente TENS, Estimulação nervosa \
            elétrica transcutânea (Transcutaneous Electrical Nerve Stimulation) tem uma duração de pulso \
                curto e é capaz de estimular fortemente fibras nervosas da pele. A TENS é uma corrente \
                    clássica no tratamento da dor via estimulação sensorial e o o estímulo é bem tolerado \
                        pelo paciente, mesmo em intensidades relativamente elevadas."


class FES(Current):
    fase = models.FloatField()
    rise = models.FloatField()
    on = models.FloatField()
    decay = models.FloatField()
    off = models.FloatField()

    def wave(self):
        """Create an array that corresponds to a FES Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        self.duty = 2 * self.fase * self.carrier * 1e-6
        return self.square(1 / (2 * self.fase)) * self.burst(self.carrier, self.duty) * self.ramp(self.rise, self.on,
                                                                                                  self.decay, self.off)

    def __str__(self):
        return "A corrente FES - Estimulação Elétrica Funcional (Function Electrical Stimulation) usa \
            estímulos elétricos de baixa frequência para produzir movimentos funcionais ou série de \
                movimentos perdidos por lesões e/ou comprometimento do sistema nervoso."


class ITP(Current):

    class Sweep(models.IntegerChoices):
        mode1 = 1
        mode2 = 2
        mode3 = 3

    AMF = models.FloatField()
    sweep_hz = models.FloatField()
    sweep_s = models.IntegerField(choices=Sweep.choices)

    def sinusoidalSecondWave(self):
        """"Create an array that corresponds to a second sinusoidal wave, which frequency is higher
        than the first one and create a beat frequency

        Returns
        -------
        array
            a array that corresponds to the value of the current on time
       """
        t = self.get_t()
        sinusoidalWave = self.intensity * np.sin(2 * np.pi * ((self.carrier + self.AMF) * t + self.sweep_mode()))

        return sinusoidalWave

    def sweep_mode(self):
        """"Create an array that corresponds to the value to be incresead at the frequency of the current,
        i. e., the sweep frequency on time depending on the sweep mode

        Returns
        -------
        array
            a array that corresponds to the value of the frequency on time
       """
        t = self.get_t()
        sweep_vector = self.sweep_hz * np.ones(len(t))
        if self.sweep_s == 1:
            return self.ramp(1, 0, 1, 0) * sweep_vector
        elif self.sweep_s == 2:
            return self.ramp(1, 5, 1, 0) * sweep_vector
        elif self.sweep_s == 3:
            return self.ramp(6, 0, 6, 0) * sweep_vector

    def wave(self):
        """Create an array that corresponds to a Interferential Tetrapolar Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        return self.sinusoidal((self.carrier + self.sweep_mode())) + self.sinusoidalSecondWave()

    def __str__(self):
        return "A corrente Interferencial Tetrapolar (ITP) é uma forma de onda de média frequência distribuída \
            através de dois canais (quatro eletrodos/4 polos). As correntes sofrem interferência no \
                ponto de cruzamento dos canais, resultando em modulação da intensidade (a intensidade \
                    da corrente aumenta e diminui em uma frequência regular)."


class IBP(Current):

    class Sweep(models.IntegerChoices):
        Modo1 = 1
        Modo2 = 2
        Modo3 = 3

    AMF = models.FloatField()
    sweep_hz = models.FloatField()
    sweep_s = models.IntegerField(choices=Sweep.choices)
    rise = models.FloatField()
    on = models.FloatField()
    decay = models.FloatField()
    off = models.FloatField()

    def sinusoidalSecondWave(self):
        """"Create an array that corresponds to a second sinusoidal wave, which frequency is higher
        than the first one, and create a beat frequency

        Returns
        -------
        array
            a array that corresponds to the value of the current on time
       """
        t = self.get_t()
        sinusoidalWave = self.intensity * np.sin(2 * np.pi * ((self.carrier + self.AMF) * t + self.sweep_mode()))

        return sinusoidalWave

    def sweep_mode(self):
        """"Create an array that corresponds to the value to be incresead at the frequency of the current,
        i. e., the sweep frequency on time, depending on the sweep mode

        Returns
        -------
        array
            a array that corresponds to the value of the frequency on time
       """
        t = self.get_t()
        sweep_vector = self.sweep_hz * np.ones(len(t))
        if self.sweep_s == 1:
            return self.ramp(1, 0, 1, 0) * sweep_vector
        elif self.sweep_s == 2:
            return self.ramp(1, 5, 1, 0) * sweep_vector
        elif self.sweep_s == 3:
            return self.ramp(6, 0, 6, 0) * sweep_vector

    def wave(self):
        """Create an array that corresponds to a Interferential Bipolar Current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        return (self.sinusoidal(self.carrier + self.sweep_mode()) + self.sinusoidalSecondWave()) * self.ramp(self.rise,
                                                                                                             self.on,
                                                                                                             self.decay,
                                                                                                             self.off)

    def __str__(self):
        return "A corrente Interferencial Bipolar IBP (pré-modulada 2 polos) é uma forma de onda \
            premodulada de média frequência distribuída através de cada canal. A intensidade de corrente \
                é modulada: aumenta e diminui em uma frequência regular (Frequência de Amplitude Modulada)."


class Microcorrente(Current):
    polo = models.CharField(max_length=2,choices=[('P+','Positivo'), ('P-','Negativo'), ('A','Alternado')])
    frequency = models.FloatField()

    def alternatingCurrent(self):
        """"Create an array that corresponds to a unitary square wave, which frequency is 0.33Hz

        Returns
        -------
        array
            a array that corresponds to the value of the current on time
       """
        t = self.get_t()
        self.freq_alt = 1 / 3;
        alt = signal.square(2 * np.pi * self.freq_alt * t, duty=0.5)

        return alt

    def wave(self):
        """Create an array that corresponds to a microcurrent on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """

        self.carrier = 15000

        if self.polo == "P+":
            return self.burst(self.carrier, 0.5) * self.burst(self.frequency, 0.5) * self.intensity

        elif self.polo == "P-":
            return self.burst(self.carrier, 0.5) * self.burst(self.frequency, 0.5) * -self.intensity

        elif self.polo == "A":
            return self.burst(self.carrier, 0.5) * self.burst(self.frequency,
                                                              0.5) * self.alternatingCurrent() * self.intensity

    def __str__(self):
        return "A Microcorrente (MENS Microcurrent Electrical Neuromuscular Stimulation) é uma forma \
            de onda monofásica ou alternada de intensidade muito baixa (μA), abaixo do limiar sensorial \
                que simula os potenciais elétricos gerados pelo corpo humano."


class Polarizada(Current):

    polo = models.CharField(max_length=2,choices=[('P+','Positivo'), ('P-','Negativo'), ('A','Alternado')])

    def wave(self):
        """Create an array that corresponds to a polarized current on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        self.carrier = 15000
        t = self.get_t(10e-8)
        sinusoidal = self.intensity * np.sin(2 * np.pi * self.carrier * t)
        if self.polo == "P+":
            return abs(sinusoidal)
        elif self.polo == "P-":
            return abs(sinusoidal) * -1

    def __str__(self):
        return "A corrente polarizada é uma corrente sinusoidal com retificação de meia onda que flui \
            em apenas um sentido."


class CPAV(Current):

    polo = models.CharField(max_length=2, choices=[('P+', 'Positivo'), ('P-', 'Negativo'), ('A', 'Alternado')])
    rise = models.FloatField()
    on = models.FloatField()
    decay = models.FloatField()
    off = models.FloatField()

    def wave(self):
        """Create an array that corresponds to a High Voltage Pulsed Stimulation on time

        Returns
        -------
        array
            a array that corresponds to the value of the current during the treatment
        """
        self.carrier_cpav = 1e4
        self.duty = self.freq / self.carrier_cpav
        if self.polo == "P+":
            return abs(self.sinusoidal(self.carrier_cpav)) * self.burst(self.carrier, self.duty) * self.ramp(self.rise, self.on,
                                                                                                     self.decay,
                                                                                                     self.off)
        elif self.polo == "P-":
            return abs(self.sinusoidal(self.carrier_cpav)) * self.burst(self.carrier, self.duty) * self.ramp(self.rise, self.on,
                                                                                                     self.decay,
                                                                                                     self.off) * -1

    def __str__(self):
        return "A CPAV (Corrente Pulsada de Alta Voltagem) conhecida também como HVPS (High Voltage \
            Pulsed Stimulation) é uma corrente senoidal monofásica (a corrente flui em uma única direção) \
                com pulsos gêmeos de alta amplitude (alta voltagem) e curta duração. A alta voltagem provoca uma \
                    diminuição da resistência da pele tornando a corrente confortável e tolerável."

