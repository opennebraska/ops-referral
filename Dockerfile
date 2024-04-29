FROM python
RUN pip install "pandas[excel]"
RUN mkdir /home/report
RUN mkdir /home/data

ARG src="OPS Referral Data 2018-2019.xlsx"
COPY ${src} /home
COPY hello.py /home
WORKDIR /home
CMD python /home/hello.py

