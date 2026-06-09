FROM node:20-alpine

WORKDIR /app

# Local packages must exist before npm ci (package.json uses file:../../packages/*)
COPY packages/api-client /packages/api-client
COPY packages/ui-kit /packages/ui-kit

COPY apps/web/package.json apps/web/package-lock.json ./

RUN npm ci --ignore-scripts

COPY apps/web .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]