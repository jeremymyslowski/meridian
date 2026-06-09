FROM node:20-alpine

WORKDIR /app

COPY packages/api-client /packages/api-client
COPY apps/web/package.json apps/web/package-lock.json* ./

RUN npm install

COPY apps/web .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]